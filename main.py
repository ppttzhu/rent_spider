import importlib
import logging
import sys
import time
import traceback
from collections import defaultdict

from playwright.sync_api import sync_playwright

import constants as c
from database import Database
from utils.init_driver import init_driver
from utils.send_mail import send_email, send_notification_email


def main():
    with sync_playwright() as play:
        driver, browser = init_driver(), None
        if c.PLATFORM != c.Platform.PYTHONANYWHERE:
            browser = play.firefox.launch(headless=False)  # headless will be blocked
        logging.info("-------------- Start Fetching Task -------------- ")
        logging.info(f"Target websites: {', '.join(c.WEBSITES_TARGETS)}")
        all_rooms = {}
        for key in c.WEBSITES_TARGETS:
            parent_class_name = c.WEBSITES_DICT[key].get("parent_class_name", key)
            fetch_class = getattr(
                importlib.import_module(f"fetch.fetch{parent_class_name}"),
                f"Fetch{parent_class_name}",
            )
            fetch_controller = fetch_class(key, driver, browser)
            rooms = fetch_controller.fetch()
            all_rooms[fetch_controller.website_name] = rooms
        if driver:
            driver.quit()
        if browser:
            browser.close()
    database = Database()
    new_rooms, removed_rooms, updated_rooms = database.update(all_rooms)
    if new_rooms or removed_rooms or updated_rooms:
        send_notification_email(new_rooms, removed_rooms, updated_rooms)
    else:
        logging.info("Nothing new to send")
    database.quit()


logging.getLogger("WDM").setLevel(logging.ERROR)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%m/%d/%Y %I:%M:%S",
)

logging.info(f"Running on {c.PLATFORM} mode...")


# deprecated
def main_in_loop():
    start_time = time.time()
    while time.time() - start_time < c.TOTAL_DURATION_IN_MINUTES * 60:
        try:
            main()
        except Exception as error:
            logging.error(repr(error))
            traceback.print_exc()
        if c.PLATFORM != c.Platform.PYTHONANYWHERE or c.RENT_TYPE == c.RentType.SUBLEASE:
            sys.exit()
        logging.info(f"Sleep for {c.MINUTES_BETWEEN_FETCH} mins...")
        time.sleep(c.MINUTES_BETWEEN_FETCH * 60)


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


if c.IS_CVS_SNAPSHOT:
    send_snapshot_email()
else:
    main()
