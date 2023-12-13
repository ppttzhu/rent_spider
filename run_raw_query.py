import csv

import constants as c
from database import Database


def run_raw_query():
    database = Database()
    columns = c.WEBSITE_ROOM_VIEW_COLUMNS + [c.FETCH_DATE_COLUMN]

    columns = c.ROOM_TABLE_COLUMNS + [
        c.WEBSITE_URL_COLUMN,
        c.WEBSITE_PRIORITY_COLUMN,
        c.FETCH_DATE_COLUMN,
    ]
    select_sql = f"""SELECT {",".join(columns)} FROM {c.WEBSITE_ROOM_HISTORY_VIEW_NAME} WHERE {c.WEBSITE_NAME_COLUMN} = 'Tower 28' and fetch_date > '2023-11-11' ORDER BY {c.FETCH_DATE_COLUMN} DESC"""

    database.cursor.execute(select_sql)
    rows = database.cursor.fetchall()
    filename = "../export.csv"
    with open(filename, "w") as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(columns)
        csvwriter.writerows(rows)


run_raw_query()
