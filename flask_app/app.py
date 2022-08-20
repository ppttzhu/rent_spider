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
    return render_template(
        "table.html",
        title=f"全部房源({len(rooms)})",
        rooms=rooms,
        headers=c.ROOM_TABLE_COLUMNS_NAME + [c.ROOM_FETCH_DATE_COLUMN_NAME],
        columns=c.WEBSITE_ROOM_VIEW_COLUMNS + [c.ROOM_FETCH_DATE_COLUMN],
    )


def get_rooms():
    database = Database()
    columns = c.WEBSITE_ROOM_VIEW_COLUMNS + [c.ROOM_FETCH_DATE_COLUMN]
    rooms = database.get_rooms(columns=columns)
    return rooms


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)
