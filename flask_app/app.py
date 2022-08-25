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
        "table.html",
        title=f"全部房源({len(rooms)})",
        rooms=rooms,
        headers=c.ROOM_TABLE_COLUMNS_NAME + [c.ROOM_FETCH_DATE_COLUMN_NAME],
        columns=c.WEBSITE_ROOM_VIEW_COLUMNS + [c.ROOM_FETCH_DATE_COLUMN],
        summary_title=f"房源网站数量汇总({len(c.WEBSITES)})",
        summary_headers=[c.ROOM_TABLE_COLUMNS_NAME[0], "房源数量", "抓取频率"],
        summary_rooms=summary_rooms,
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
            "frequency": "每日两次" if web["platform"] == c.Platform.AWS else "几分钟一次",
            c.WEBSITE_PRIORITY_COLUMN: index,
            c.WEBSITE_URL_COLUMN: web[c.WEBSITE_URL_COLUMN],
        }
        for index, web in enumerate(c.WEBSITES)
    }
    for room in rooms:
        summary_rooms[room[c.ROOM_WEBSITE_NAME_COLUMN]]["count"] += 1
    return summary_rooms


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)
