import importlib
import logging
import time
import traceback

from playwright.sync_api import sync_playwright

import constants as c
from database import Database
from utils.init_driver import init_driver
from utils.send_mail import send_notification_email_summer


def main():
    with sync_playwright() as play:
        driver, browser = init_driver(), None
        if c.PLATFORM not in [c.Platform.PYTHONANYWHERE, c.Platform.PYTHONANYWHERE_2]:
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
        # send_notification_email(new_rooms, removed_rooms, updated_rooms)
        send_notification_email_summer(new_rooms, removed_rooms, updated_rooms)
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


def main_in_loop():
    start_time = time.time()
    while True:
        last_iteration_start_time = time.time()
        try:
            main()
        except Exception as error:
            logging.error(repr(error))
            traceback.print_exc()
        one_loop_duration = time.time() - last_iteration_start_time
        logging.info(f"Last iter takes {one_loop_duration//60} mins...")
        if time.time() + one_loop_duration > start_time + c.TOTAL_DURATION_IN_MINUTES * 60:
            # No time to finish a new iteration
            break
        else:
            time_sleep_in_mins = max(c.MINUTES_BETWEEN_FETCH - one_loop_duration // 60, 0)
            logging.info(f"Sleep for {time_sleep_in_mins} mins...")
            time.sleep(time_sleep_in_mins * 60)


if c.PLATFORM == c.Platform.PYTHONANYWHERE_2 or c.RENT_TYPE == c.RentType.SUBLEASE:
    main_in_loop()
else:
    main()
