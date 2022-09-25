import json
import os
import sys
from typing import DefaultDict

root_dir = os.path.join(os.path.dirname(__file__), "../")

sys.path.append(root_dir)  # For module not found error

import constants as c
from database import Database
from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def index():
    return room_with_location_filter()


@app.route("/lic")
def rooms_in_lic():
    return room_with_location_filter("LIC")


@app.route("/nj")
def rooms_in_nj():
    return room_with_location_filter("NJ")


def room_with_location_filter(location=None):
    rooms = get_rooms()
    if location:
        rooms = [room for room in rooms if room[c.WEBSITE_LOCATION_COLUMN] == location]
    summary_rooms = get_summary_rooms(rooms, location)
    return render_template(
        "rooms.html",
        id=f"{location or 'home'}",
        title=f"{location or '全部房源'}({len(rooms)})",
        rooms=rooms,
        headers=c.ROOM_TABLE_COLUMNS_NAME + [c.ROOM_FETCH_DATE_COLUMN_NAME],
        columns=c.WEBSITE_ROOM_VIEW_COLUMNS + [c.ROOM_FETCH_DATE_COLUMN],
        summary_title=f"房源网站数量汇总({len(summary_rooms)})",
        summary_headers=[c.ROOM_TABLE_COLUMNS_NAME[0], c.ROOM_COUNT_COLUMN_NAME, "抓取频率"],
        summary_rooms=summary_rooms,
    )


@app.route("/statistics")
def statistics_page():
    room_history = get_room_history()
    return render_template(
        "statistics.html",
        id="statistics",
        title=f"房源信息统计({len(room_history)})",
        room_history=room_history,
        headers=c.ROOM_TABLE_COLUMNS_NAME + [c.ROOM_FETCH_DATE_COLUMN_NAME],
        columns=c.WEBSITE_ROOM_VIEW_COLUMNS + [c.ROOM_FETCH_DATE_COLUMN],
    )


@app.route("/fetch-status")
def fetch_status_page():
    fetch_status = get_fetch_status()
    group_by_website = DefaultDict(list)
    for record in fetch_status:
        group_by_website[record[c.ROOM_WEBSITE_NAME_COLUMN]].append(
            {
                "x": record[c.ROOM_FETCH_DATE_COLUMN].strftime("%Y-%m-%d %H:%M:%S"),
                "y": record[c.FETCH_STATUS_ROOM_COUNT_COLUMN],
            }
        )
    return render_template(
        "fetch_status.html",
        id="fetch_status",
        title="抓取记录",
        fetch_status=fetch_status,
        group_by_website=group_by_website,
    )


def get_rooms():
    database = Database()
    columns = c.WEBSITE_ROOM_VIEW_COLUMNS + [c.ROOM_FETCH_DATE_COLUMN]
    rooms = database.get_rooms(columns=columns)
    return rooms


def get_summary_rooms(rooms, location=None):
    summary_rooms = {
        web[c.ROOM_WEBSITE_NAME_COLUMN]: {
            "count": 0,
            "frequency": "每日12点和19点" if web["platform"] == c.Platform.AWS else "几分钟一次",
            c.WEBSITE_PRIORITY_COLUMN: index,
            c.WEBSITE_URL_COLUMN: web[c.WEBSITE_URL_COLUMN],
        }
        for index, web in enumerate(c.WEBSITES)
        if (True if not location else web[c.WEBSITE_LOCATION_COLUMN] == location)
    }
    for room in rooms:
        summary_rooms[room[c.ROOM_WEBSITE_NAME_COLUMN]]["count"] += 1
    return summary_rooms


def get_room_history():
    database = Database()
    return database.get_room_history()


def get_fetch_status():
    database = Database()
    return database.get_fetch_status()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)
