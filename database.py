import configparser
import logging
import os
from collections import defaultdict
from datetime import datetime

import MySQLdb
from pytz import timezone
from sshtunnel import SSHTunnelForwarder

import constants as c


class Database:
    def __init__(self):
        logging.info("Init DB...")
        config = configparser.ConfigParser()
        config.read(os.path.join(c.ROOT_DIR, "secrets.cfg"))
        if c.PLATFORM == c.Platform.AWS:
            logging.info("Opening SSH tunnel...")
            tunnel = SSHTunnelForwarder(
                c.SSH_HOST,
                ssh_username=c.SSH_USERNAME,
                ssh_password=config["ssh"]["password"],
                remote_bind_address=(c.SSH_REMOTE_BIND_ADDRESS, c.SSH_REMOTE_BIND_PORT),
            )
            tunnel.start()
            self.tunnel = tunnel
            conn = MySQLdb.connect(
                user=c.DATABASE_USER,
                passwd=config["database"]["password"],
                host="127.0.0.1",
                port=tunnel.local_bind_port,
                db=c.DATABASE_NAME,
            )
        else:
            conn = MySQLdb.connect(
                host="127.0.0.1" if c.PLATFORM == c.Platform.DEV else c.DATABASE_HOST,
                user="root" if c.PLATFORM == c.Platform.DEV else c.DATABASE_USER,
                passwd=config["database"]["password"],
                db=c.DATABASE_NAME,
            )
        self.conn = conn
        self.cursor = conn.cursor()

    def quit(self):
        logging.info("Disconnecting DB...")
        self.cursor.close()
        self.conn.close()
        if c.PLATFORM == c.Platform.AWS:
            self.tunnel.stop()

    def update(self, cur_rooms, succeeded_websites):
        # TODO: collect statistics
        if c.NEED_UPDATE_WEBSITE:
            self.update_website()
        if not succeeded_websites:
            return [], [], []
        prev_rooms = self.get_rooms(websites=succeeded_websites)
        new_rooms, removed_rooms, updated_rooms = self.compare_rooms_diff(prev_rooms, cur_rooms)
        for room in new_rooms:
            self.create_room(room)
        for room in removed_rooms:
            self.delete_room(room)
        for prev_room, cur_room in updated_rooms:
            self.update_room(prev_room, cur_room)
        logging.info(f"Previous rooms number: {len(prev_rooms)}")
        logging.info(f"Current rooms number: {len(cur_rooms)}")
        logging.info(f"New rooms number: {len(new_rooms)}")
        logging.info(f"Removed rooms number: {len(removed_rooms)}")
        logging.info(f"Updated rooms number: {len(updated_rooms)}")
        return new_rooms, removed_rooms, updated_rooms

    def compare_rooms_diff(self, prev_rooms, cur_rooms):
        def get_primary_key(room):
            return tuple([room[column] for column in c.ROOM_TABLE_PRIMARY_KEY])

        def get_info(room):
            return tuple([room[column] for column in c.ROOM_TABLE_COLUMNS])

        prev_rooms_pk_set, cur_rooms_pk_set = set(), set()
        prev_rooms_info_set, cur_rooms_info_set = set(), set()
        for room in prev_rooms:
            prev_rooms_pk_set.add(get_primary_key(room))
            prev_rooms_info_set.add(get_info(room))
        for room in cur_rooms:
            cur_rooms_pk_set.add(get_primary_key(room))
            cur_rooms_info_set.add(get_info(room))

        new_rooms, removed_rooms, updated_rooms = [], [], defaultdict(dict)
        for room in prev_rooms:
            key = get_primary_key(room)
            info = get_info(room)
            if key not in cur_rooms_pk_set:
                removed_rooms.append(room)
            elif info not in cur_rooms_info_set:
                updated_rooms[key]["prev_room"] = room
        for room in cur_rooms:
            key = get_primary_key(room)
            info = get_info(room)
            if key not in prev_rooms_pk_set:
                new_rooms.append(room)
            elif info not in prev_rooms_info_set:
                updated_rooms[key]["cur_room"] = room

        updated_rooms = [(room["prev_room"], room["cur_room"]) for room in updated_rooms.values()]
        return new_rooms, removed_rooms, updated_rooms

    def get_rooms(self, columns=None, websites=None):
        if not columns:
            columns = c.WEBSITE_ROOM_VIEW_COLUMNS
        order_by = [
            c.WEBSITE_PRIORITY_COLUMN,
            c.ROOM_ROOM_TYPE_COLUMN,
            c.ROOM_MOVE_IN_DATE_COLUMN,
            c.ROOM_ROOM_PRICE_COLUMN,
        ]
        condition = ""
        if websites:
            condition = f"""WHERE {c.WEBSITE_NAME_COLUMN} in ('{("','").join(websites)}')"""
        select_sql = f"""SELECT {",".join(columns)} FROM {c.WEBSITE_ROOM_VIEW_NAME} {condition} ORDER BY {",".join(order_by)}"""
        self.cursor.execute(select_sql)
        rows = self.cursor.fetchall()
        rooms = []
        for row in rows:
            room = {}
            for idx, column in enumerate(columns):
                room[column] = row[idx]
            rooms.append(room)
        return rooms

    def create_room(self, room):
        columns = c.ROOM_TABLE_COLUMNS + [c.ROOM_FETCH_DATE_COLUMN]
        values = [room[column] for column in c.ROOM_TABLE_COLUMNS] + [
            datetime.now(timezone("US/Eastern")).strftime("%Y-%m-%d %H:%M:%S")
        ]
        insert_sql = f"""INSERT INTO {c.ROOM_TABLE_NAME} ({",".join(columns)}) VALUES ('{"','".join(values)}')"""
        try:
            self.cursor.execute(insert_sql)
            self.conn.commit()
        except Exception:
            logging.error(f"Failed to execute {insert_sql}")
            raise

    def delete_room(self, room):
        condition = " AND ".join(
            [f"{column} = '{room[column]}'" for column in c.ROOM_TABLE_PRIMARY_KEY]
        )
        delete_sql = f"DELETE FROM {c.ROOM_TABLE_NAME} WHERE {condition}"
        try:
            self.cursor.execute(delete_sql)
            self.conn.commit()
        except Exception:
            logging.error(f"Failed to execute {delete_sql}")
            raise

    def update_room(self, prev_room, cur_room):
        condition = " AND ".join(
            [f"{column} = '{prev_room[column]}'" for column in c.ROOM_TABLE_PRIMARY_KEY]
        )
        non_primary_key = [
            column for column in c.ROOM_TABLE_COLUMNS if column not in c.ROOM_TABLE_PRIMARY_KEY
        ]
        cur_values = []
        for column in non_primary_key:
            cur_values.append(f"{column} = '{cur_room[column]}'")
        update_sql = f"""UPDATE {c.ROOM_TABLE_NAME} SET {",".join(cur_values)} WHERE {condition}"""
        try:
            self.cursor.execute(update_sql)
            self.conn.commit()
        except Exception:
            logging.error(f"Failed to execute {update_sql}")
            raise

    def update_website(self):
        logging.info("Updating website info...")
        cur_website_name = [website[c.WEBSITE_NAME_COLUMN] for website in c.WEBSITES]
        # Delete from database if not exist in constants
        select_sql = f"""SELECT {c.WEBSITE_NAME_COLUMN} FROM {c.WEBSITE_TABLE_NAME}"""
        self.cursor.execute(select_sql)
        rows = self.cursor.fetchall()
        to_be_deleted = [row[0] for row in rows if row[0] not in cur_website_name]
        if to_be_deleted:
            delete_sql = f"""DELETE FROM {c.WEBSITE_TABLE_NAME} WHERE {c.WEBSITE_NAME_COLUMN} IN ('{"','".join(to_be_deleted)}')"""
            try:
                self.cursor.execute(delete_sql)
                self.conn.commit()
            except Exception:
                logging.error(f"Failed to execute {delete_sql}")
                raise
        # Update or insert if it is new
        for idx, website in enumerate(c.WEBSITES):
            website_name = website[c.WEBSITE_NAME_COLUMN]
            url = website[c.WEBSITE_URL_COLUMN]
            update_sql = f"""INSERT INTO {c.WEBSITE_TABLE_NAME} ({c.WEBSITE_NAME_COLUMN}, {c.WEBSITE_URL_COLUMN}, {c.WEBSITE_PRIORITY_COLUMN}) VALUES('{website_name}', '{url}', {idx}) ON DUPLICATE KEY UPDATE {c.WEBSITE_URL_COLUMN}='{url}', {c.WEBSITE_PRIORITY_COLUMN}={idx}"""
            try:
                self.cursor.execute(update_sql)
                self.conn.commit()
            except Exception:
                logging.error(f"Failed to execute {update_sql}")
                raise
