from datetime import datetime, timedelta

import constants as c
from database import Database
from utils.send_mail import send_notification_email_summer


def send_daily_email():
    database = Database()
    columns = c.WEBSITE_ROOM_VIEW_COLUMNS + [c.FETCH_DATE_COLUMN]
    rooms = database.get_rooms(columns=columns)

    # filter rooms with fetch_date with in 24 hours
    now = datetime.now()
    rooms = [room for room in rooms if now - timedelta(hours=24) <= room["fetch_date"]]

    location_set = set()
    for web in c.WEBSITES:
        location_set.add(web["location"])

    for location in location_set:
        filtered_room = [room for room in rooms if room["location"] == location]
        send_notification_email_summer(filtered_room, [], [], True, location)


send_daily_email()
