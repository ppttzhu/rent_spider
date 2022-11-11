import logging
import re
import traceback
from time import sleep

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

import constants as c


class Fetch:
    def __init__(self, driver, browser):
        self.driver = driver
        self.browser = browser

        web_key = self.__class__.__name__.replace("Fetch", "")
        self.url = c.WEBSITES_DICT[web_key][c.WEBSITE_URL_COLUMN]
        self.website_name = c.WEBSITES_DICT[web_key][c.WEBSITE_NAME_COLUMN]
        self.priority = c.WEBSITES_DICT[web_key][c.WEBSITE_PRIORITY_COLUMN]

        self.room_type_map = None
        self.room_info = []
        self.room_info_tuple_set = set()  # Avoid duplicate value
        self.web_wait = WebDriverWait(self.driver, c.WEB_DRIVER_WAIT_SECOND)

    def fetch(self):
        try:
            self.fetch_web()
            logging.info(f"{self.website_name} rooms number: {len(self.room_info)}")
            return self.room_info
        except Exception as error:
            self.report_error(error)
            return None

    def fetch_web(self):
        raise NotImplementedError("Must override abstract method")

    def report_error(self, error):
        logging.error(f"Fetch Rooms Error in {self.website_name}")
        logging.error(repr(error))
        traceback.print_exc()

    def add_room_info(self, room_number, room_type, move_in_date, room_price):
        if not room_number or not room_type or not move_in_date or not room_price:
            raise Exception(
                f"Should not have empty value: room_number={room_number}, room_type={room_type}, move_in_date={move_in_date}, room_price={room_price}"
            )
        room = {
            c.WEBSITE_URL_COLUMN: self.url,
            c.WEBSITE_PRIORITY_COLUMN: self.priority,
            c.WEBSITE_NAME_COLUMN: self.website_name,
            c.ROOM_NUMBER_COLUMN: self.process_room_number(room_number),
            c.ROOM_TYPE_COLUMN: self.process_room_type(room_type),
            c.MOVE_IN_DATE_COLUMN: self.process_move_in_date(move_in_date),
            c.ROOM_PRICE_COLUMN: self.process_room_price(room_price),
        }
        room_info_tuple = tuple([room_number, room_type, move_in_date, room_price])
        if room_info_tuple in self.room_info_tuple_set:
            return
        logging.debug(room)
        self.room_info.append(room)
        self.room_info_tuple_set.add(room_info_tuple)

    def add_sublease_info(self, sublease_info):
        self.room_info.append(
            {
                **sublease_info,
                c.WEBSITE_NAME_COLUMN: self.website_name,
            }
        )

    def save_html_doc(self, html_doc):
        with open("./tmp.html", "w", encoding="utf-8") as file:
            file.write(html_doc)

    def process_room_price(self, room_price):
        return room_price.replace.replace(",", "").replace(".00", "")

    def process_room_number(self, room_number):
        return room_number.replace("Apartment:", "").replace("#", "").replace("\n", "")

    def process_room_type(self, room_type):
        ret = room_type
        for re_rule, type_value in self.room_type_map or []:
            if re.search(re_rule, room_type):
                ret = type_value
                break
        ret = ret.replace("Studio", "0Studio")  # To make Studio appear at the first
        return ret

    def process_move_in_date(self, move_in_date):
        if "Available Now" in move_in_date:
            return "Available Now"
        return move_in_date.replace(" ", "").replace("\n", "")

    # pw
    def init_page(self):
        self.page = self.browser.new_page()
        # don't load image and avoid doubleclick request
        self.page.route(
            re.compile(r"(\.png$)|(\.jpg$)|(\.webp$)|(doubleclick)"), lambda route: route.abort()
        )
        return self.page

    # pw
    def get_html_doc(self, url, wait_until="domcontentloaded"):
        logging.info(f"Loading {url}...")
        self.page.goto(url, wait_until=wait_until, timeout=c.WEB_DRIVER_WAIT_SECOND * 60 * 1000)
        return self.page.content()

    # se
    def wait_until_xpath(self, xpath, driver=None):
        if not driver:
            driver = self.driver
        waiter = WebDriverWait(driver, c.WEB_DRIVER_WAIT_SECOND)
        waiter.until(EC.presence_of_element_located((By.XPATH, xpath)))
        return driver.find_elements(by=By.XPATH, value=xpath)

    # se
    def get_url_with_retry(self, url):
        count = 0
        max_retry = 3
        sleep_second = 1
        while True:
            try:
                self.driver.get(url)
                return
            except Exception as error:
                count += 1
                if count > max_retry:
                    raise
                logging.error(f"Caught {type(error).__name__} in {url}, retry {count}...")
                sleep(sleep_second)
