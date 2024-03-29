import os
import sys
from datetime import datetime, timedelta
from typing import DefaultDict

root_dir = os.path.join(os.path.dirname(__file__), "../")

sys.path.append(root_dir)  # For module not found error

from flask import Flask, render_template

import constants as c
from database import Database

app = Flask(__name__)


@app.route("/")
def index():
    return room_with_location_filter()


@app.route("/lic")
def rooms_in_lic():
    return room_with_location_filter("LIC")


@app.route("/manhattan")
def rooms_in_manhattan():
    return room_with_location_filter("Manhattan")


@app.route("/nj")
def rooms_in_nj():
    return room_with_location_filter("NJ")


@app.route("/nj2")
def rooms_in_nj2():
    return room_with_location_filter("NJ2")


@app.route("/npr")
def rooms_in_npr():
    return room_with_location_filter("NPR")


@app.route("/tfc-chelsea")
def rooms_in_tfc_chelsea():
    return room_with_location_filter("TFCChelsea")


@app.route("/tfc-others")
def rooms_in_tfc_others():
    return room_with_location_filter("TFCOthers")


@app.route("/cu")
def rooms_in_cu():
    return room_with_location_filter("CU")


@app.route("/elmhurst")
def rooms_in_elmhurst():
    return room_with_location_filter("Elmhurst")


@app.route("/bk")
def rooms_in_bk():
    return room_with_location_filter("BK")


@app.route("/bklow")
def rooms_in_bklow():
    return room_with_location_filter("BKLow")


def apply_location_override_rules(rooms):
    max_lyra_index = 0
    hudson_indices = []
    for idx, room in enumerate(rooms):
        if room[c.ROOM_NUMBER_COLUMN].startswith("[Long Island City]"):
            room[c.WEBSITE_LOCATION_COLUMN] = "LIC"
        if room[c.ROOM_NUMBER_COLUMN].startswith("[Hudson Yards]"):
            room[c.WEBSITE_LOCATION_COLUMN] = "Manhattan"
            hudson_indices.append(idx)
        if room[c.WEBSITE_NAME_COLUMN] == "Lyra":
            max_lyra_index = idx
    for idx in hudson_indices:
        rooms.insert(max_lyra_index + 1, rooms.pop(idx))


def room_with_location_filter(location=None):
    rooms = get_rooms()
    latest_fetch_status = get_latest_fetch_status()
    latest_fetch_status_dict = {
        record[c.WEBSITE_NAME_COLUMN]: record[c.FETCH_DATE_COLUMN] for record in latest_fetch_status
    }
    apply_location_override_rules(rooms)
    if location:
        rooms = [room for room in rooms if room[c.WEBSITE_LOCATION_COLUMN] == location]
    for room in rooms:
        room[c.LATEST_FETCH_DATE_COLUMN] = latest_fetch_status_dict.get(room[c.WEBSITE_NAME_COLUMN])
        room[c.LATEST_FETCH_WARNING] = not room[c.LATEST_FETCH_DATE_COLUMN] or room[
            c.LATEST_FETCH_DATE_COLUMN
        ] < datetime.now() - timedelta(days=1)
    summary_rooms = get_summary_rooms(rooms, location, c.RentType.RENTAL)
    for web_name, summary in summary_rooms.items():
        summary[c.LATEST_FETCH_DATE_COLUMN] = latest_fetch_status_dict.get(web_name)
        summary[c.LATEST_FETCH_WARNING] = not summary[c.LATEST_FETCH_DATE_COLUMN] or summary[
            c.LATEST_FETCH_DATE_COLUMN
        ] < datetime.now() - timedelta(days=1)
    webs_with_error = [
        web_name for web_name, summary in summary_rooms.items() if summary[c.LATEST_FETCH_WARNING]
    ]
    error_message = (
        ""
        if not webs_with_error
        else f"Found {len(webs_with_error)} failed fetch: {','.join(webs_with_error)}"
    )

    return render_template(
        "rooms.html",
        id=f"{location or 'home'}",
        title=f"{location or '全部房源'}({len(rooms)})",
        error_message=error_message,
        rooms=rooms,
        headers=c.ROOM_TABLE_COLUMNS_NAME
        + [c.FETCH_DATE_COLUMN_NAME, c.LATEST_FETCH_DATE_COLUMN_NAME],
        columns=c.WEBSITE_ROOM_VIEW_COLUMNS + [c.FETCH_DATE_COLUMN, c.LATEST_FETCH_DATE_COLUMN],
        summary_title=f"房源网站数量汇总({len(summary_rooms)})",
        summary_headers=[
            c.ROOM_TABLE_COLUMNS_NAME[0],
            c.ROOM_COUNT_COLUMN_NAME,
            c.FETCH_FREQUENCY_COLUMN_NAME,
            c.LATEST_FETCH_DATE_COLUMN_NAME,
        ],
        summary_rooms=summary_rooms,
    )


@app.route("/sublease")
def sublease_rooms():
    rooms = get_sublease()
    summary_rooms = get_summary_rooms(rooms, None, c.RentType.SUBLEASE)
    return render_template(
        "sublease.html",
        id="sublease",
        title=f"转租({len(rooms)})",
        rooms=rooms,
        headers=c.SUBLEASE_TABLE_COLUMNS_NAME + [c.FETCH_DATE_COLUMN_NAME],
        columns=c.SUBLEASE_TABLE_COLUMNS + [c.FETCH_DATE_COLUMN],
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
        headers=c.ROOM_TABLE_COLUMNS_NAME + [c.FETCH_DATE_COLUMN_NAME],
        columns=c.WEBSITE_ROOM_VIEW_COLUMNS + [c.FETCH_DATE_COLUMN],
    )


@app.route("/fetch-status")
def fetch_status_page():
    fetch_status = get_fetch_status()
    group_by_website = DefaultDict(list)
    fetch_status_bool = DefaultDict(list)
    for record in fetch_status:
        room_name = f"[{record[c.WEBSITE_PRIORITY_COLUMN]}] {record[c.WEBSITE_NAME_COLUMN]}"
        count = record[c.ROOM_COUNT_COLUMN]
        fetch_date = record[c.FETCH_DATE_COLUMN].strftime("%Y-%m-%d %H:%M:%S")
        fetch_status_bool[room_name].append({"x": fetch_date, "y": -1 if count == -1 else 0})
        if count != -1:
            group_by_website[room_name].append({"x": fetch_date, "y": count})
    ordered_group_by_website = {}
    for key in sorted(group_by_website.keys()):
        ordered_group_by_website[key] = group_by_website[key]
    return render_template(
        "fetch_status.html",
        id="fetch_status",
        title="抓取记录",
        fetch_status=fetch_status,
        group_by_website=ordered_group_by_website,
        fetch_status_bool=fetch_status_bool,
    )


def get_rooms():
    database = Database()
    columns = c.WEBSITE_ROOM_VIEW_COLUMNS + [c.FETCH_DATE_COLUMN]
    rooms = database.get_rooms(columns=columns)
    return rooms


def get_sublease():
    database = Database()
    rooms = database.get_sublease()
    return rooms


def get_summary_rooms(rooms, location=None, rent_type=None):
    summary_rooms = {
        web[c.WEBSITE_NAME_COLUMN]: {
            "count": 0,
            "frequency": c.FREQUENCY_MAP[web["platform"]],
            c.WEBSITE_PRIORITY_COLUMN: index,
            c.WEBSITE_URL_COLUMN: web[c.WEBSITE_URL_COLUMN],
        }
        for index, web in enumerate(c.WEBSITES)
        if (not location or web[c.WEBSITE_LOCATION_COLUMN] == location)
        and (not rent_type or web[c.WEBSITE_RENT_TYPE] == rent_type)
    }
    for room in rooms:
        if room[c.WEBSITE_NAME_COLUMN] in summary_rooms:
            summary_rooms[room[c.WEBSITE_NAME_COLUMN]]["count"] += 1
    return summary_rooms


def get_room_history():
    database = Database()
    return database.get_room_history()


def get_fetch_status():
    database = Database()
    return database.get_fetch_status()


def get_latest_fetch_status():
    database = Database()
    return database.get_latest_fetch_status()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)
