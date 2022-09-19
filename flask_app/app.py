import os
import sys

root_dir = os.path.join(os.path.dirname(__file__), "../")

sys.path.append(root_dir)  # For module not found error

import constants as c
from database import Database
from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def index():
    rooms = get_rooms()
    summary_rooms = get_summary_rooms(rooms)
    return render_template(
        "rooms.html",
        id="home",
        title=f"全部房源({len(rooms)})",
        rooms=rooms,
        headers=c.ROOM_TABLE_COLUMNS_NAME + [c.ROOM_FETCH_DATE_COLUMN_NAME],
        columns=c.WEBSITE_ROOM_VIEW_COLUMNS + [c.ROOM_FETCH_DATE_COLUMN],
        summary_title=f"房源网站数量汇总({len(c.WEBSITES)})",
        summary_headers=[c.ROOM_TABLE_COLUMNS_NAME[0], "房源数量", "抓取频率"],
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
    return render_template(
        "fetch_status.html",
        id="fetch_status",
        title="抓取是否成功",
        fetch_status=fetch_status,
        headers=c.FETCH_STATUS_COLUMNS_NAME,
        columns=c.FETCH_STATUS_COLUMNS + [c.WEBSITE_PRIORITY_COLUMN],
    )


def get_rooms():
    database = Database()
    columns = c.WEBSITE_ROOM_VIEW_COLUMNS + [c.ROOM_FETCH_DATE_COLUMN]
    rooms = database.get_rooms(columns=columns)
    return rooms


def get_summary_rooms(rooms):
    summary_rooms = {
        web[c.ROOM_WEBSITE_NAME_COLUMN]: {
            "count": 0,
            "frequency": "每日12点和19点" if web["platform"] == c.Platform.AWS else "几分钟一次",
            c.WEBSITE_PRIORITY_COLUMN: index,
            c.WEBSITE_URL_COLUMN: web[c.WEBSITE_URL_COLUMN],
        }
        for index, web in enumerate(c.WEBSITES)
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
