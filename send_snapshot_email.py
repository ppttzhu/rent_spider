from collections import defaultdict

import constants as c
from database import Database
from utils.send_mail import send_email


def send_snapshot_email():
    from openpyxl import Workbook

    database = Database()
    all_rooms = database.get_rooms()
    wb = Workbook()
    rooms_split_by_location = defaultdict(list)
    for room in all_rooms:
        rooms_split_by_location[room["location"]].append(room)
    for location, rooms in rooms_split_by_location.items():
        ws = wb.create_sheet(location)
        ws.append(list(rooms[0].keys()))
        for room in rooms:
            ws.append(list(room.values()))
    default_sheet = wb["Sheet"]
    wb.remove(default_sheet)
    wb.save(c.SNAPSHOT_DIR)
    send_email(
        c.EMAIL_RECEIVERS_DEV if c.PLATFORM == c.Platform.DEV else c.SNAPSHOT_EMAIL_RECEIVERS,
        c.EMAIL_RECEIVERS_DEV,
        c.SNAPSHOT_EMAIL_SUBJECT,
        "",
        c.SNAPSHOT_DIR,
    )
    database.quit()


send_snapshot_email()
