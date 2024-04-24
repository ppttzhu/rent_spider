import re
from datetime import datetime, timedelta

import constants as c
from database import Database
from utils.send_mail import send_notification_email_summary


def send_daily_email():
    database = Database()
    columns = c.WEBSITE_ROOM_VIEW_COLUMNS + [c.FETCH_DATE_COLUMN]
    rooms = database.get_rooms(columns=columns)

    # filter rooms with fetch_date with in 24 hours
    now = datetime.now()
    today_rooms = [room for room in rooms if now - timedelta(hours=24) <= room["fetch_date"]]

    location_set = set()
    for web in c.WEBSITES:
        location_set.add(web["location"])

    for location in location_set:
        today_location_rooms = [room for room in today_rooms if room["location"] == location]
        top_rooms = get_top_rooms(rooms, location)
        send_notification_email_summary(today_location_rooms, [], [], top_rooms, location)


def parse_price(price_string):
    try:
        return int(price_string)
    except:
        return float("inf")


def get_top_rooms(rooms, location):
    location_rooms = [room for room in rooms if room["location"] == location]
    for room in location_rooms:
        result = re.search("\$\d+", room["room_price"])
        if result:
            room["parsed_room_price"] = parse_price(result.group().replace("$", ""))
        else:
            room["parsed_room_price"] = parse_price(room["room_price"])
    location_rooms.sort(key=lambda x: (x["room_type"], x["parsed_room_price"]))
    TOP_K = 5
    top_rooms = []
    cur = 0
    previous = None
    for room in location_rooms:
        if room["website_name"] in c.TOP_5_EXCLUDE:
            continue
        if room["room_type"] != previous:
            cur = 0
            previous = room["room_type"]
        if cur < TOP_K:
            top_rooms.append(room)
        cur += 1
    return top_rooms


send_daily_email()
