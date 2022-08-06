import importlib
import logging
import sys
import time
import traceback

from playwright.sync_api import sync_playwright

import constants as c
from database import Database
from utils.init_driver import init_driver
from utils.send_mail import send_notification_email


def main():
    with sync_playwright() as play:
        driver, browser = None, None
        if c.PLATFORM != c.Platform.PYTHONANYWHERE:
            browser = play.firefox.launch(headless=False)
        if c.PLATFORM != c.Platform.AWS:
            driver = init_driver()
        logging.info("-------------- Start Fetching Task -------------- ")
        all_rooms, succeeded_websites, failed_websites = [], [], []
        logging.info(f"Target websites: {', '.join(c.WEBSITES_TARGETS)}")
        for key in c.WEBSITES_TARGETS:
            fetch_class = getattr(importlib.import_module(f"fetch.fetch{key}"), f"Fetch{key}")
            fetch_controller = fetch_class(driver, browser)
            rooms = fetch_controller.fetch()
            if fetch_controller.is_fetch_succeeded:
                all_rooms += rooms
                succeeded_websites.append(fetch_controller.website_name)
            else:
                failed_websites.append(fetch_controller.website_name)
        if driver:
            driver.quit()
        if browser:
            browser.close()
    logging.info(f"Succeeded websites ({len(succeeded_websites)}): {succeeded_websites}")
    logging.info(f"Failed websites ({len(failed_websites)}): {failed_websites}")
    database = Database()
    new_rooms, removed_rooms, updated_rooms = database.update(all_rooms, succeeded_websites)
    if new_rooms or removed_rooms or updated_rooms:
        logging.info("Sending email...")
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

start_time = time.time()
while time.time() - start_time < c.TOTAL_DURATION_IN_MINUTES * 60:
    try:
        main()
    except Exception as error:
        logging.error(repr(error))
        traceback.print_exc()
    if c.PLATFORM != c.Platform.PYTHONANYWHERE:
        sys.exit()
    logging.info(f"Sleep for {c.MINUTES_BETWEEN_FETCH} mins...")
    time.sleep(c.MINUTES_BETWEEN_FETCH * 60)
