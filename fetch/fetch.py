import logging
import os
import re
import traceback
from time import sleep

import requests
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

import constants as c
from utils.user_agent import get_random_user_agent


class Fetch:
    def __init__(self, **kwargs):
        self.web_key = kwargs.get("web_key")
        self.driver = kwargs.get("driver")
        self.browser = kwargs.get("browser")

        self.url = c.WEBSITES_DICT[self.web_key][c.WEBSITE_URL_COLUMN]
        self.website_name = c.WEBSITES_DICT[self.web_key][c.WEBSITE_NAME_COLUMN]
        self.priority = c.WEBSITES_DICT[self.web_key][c.WEBSITE_PRIORITY_COLUMN]

        self.room_type_map = None
        self.room_info = []
        self.room_info_tuple_set = set()  # Avoid duplicate value
        self.web_wait = WebDriverWait(self.driver, c.WEB_DRIVER_TIMEOUT_SECOND)
        self.html_text = ""

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
        with open(os.path.join(c.ROOT_DIR, f"logs/{self.website_name}.html"), "w") as html_file:
            html_file.write(self.html_text)

    def add_room_info(self, room_number, room_type, move_in_date, room_price, room_url=None):
        if not room_number or not room_type or not move_in_date or not room_price:
            raise Exception(
                f"Should not have empty value: room_number={room_number}, room_type={room_type}, move_in_date={move_in_date}, room_price={room_price}"
            )
        room = {
            c.WEBSITE_URL_COLUMN: self.url,
            c.WEBSITE_PRIORITY_COLUMN: self.priority,
            c.WEBSITE_NAME_COLUMN: self.website_name,
            c.ROOM_URL_COLUMN: room_url,
            c.ROOM_NUMBER_COLUMN: self.process_room_number(room_number),
            c.ROOM_TYPE_COLUMN: self.process_room_type(room_type),
            c.MOVE_IN_DATE_COLUMN: self.process_move_in_date(move_in_date),
            c.ROOM_PRICE_COLUMN: self.process_room_price(room_price),
            c.WEBSITE_LOCATION_COLUMN: c.WEBSITES_DICT[self.web_key][c.WEBSITE_LOCATION_COLUMN],
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
        return room_price.replace(",", "").replace(".00", "")

    def process_room_number(self, room_number):
        return room_number.replace("Apartment:", "").replace("#", "").replace("\n", "")

    def process_room_type(self, room_type):
        ret = room_type
        for re_rule, type_value in self.room_type_map or []:
            if re.search(re_rule, room_type):
                ret = type_value
                break
        if "studio" in ret.lower():
            return "0Studio"  # To make Studio appear at the first
        return ret

    def process_move_in_date(self, move_in_date):
        if "Available Now" in move_in_date:
            return "Available Now"
        return move_in_date.replace(" ", "").replace("\n", "")

    # pw
    def init_page(self):
        self.context = self.browser.new_context(user_agent=get_random_user_agent())
        self.page = self.context.new_page()
        return self.page

    def get_html_doc(self, url):
        if c.PLATFORM == c.Platform.DEV:
            return self.get_html_doc_with_pw(url)
        else:
            return self.get_html_doc_with_zyte(url)

    def get_html_doc_with_pw(self, url, wait_until="domcontentloaded"):
        logging.info(f"Loading {url}...")
        self.init_page()
        self.page.goto(url, wait_until=wait_until, timeout=c.WEB_DRIVER_TIMEOUT_SECOND * 1000)
        content = self.page.content()
        self.context.close()
        return content

    def get_html_doc_with_zyte(self, url):
        logging.info(f"Loading {url} with zyte...")
        count = 0
        sleep_time = 1
        while count < c.ZYTE_GET_URL_MAX_RETRY:
            response = requests.get(
                url,
                proxies={
                    "http": f"http://{c.CONFIG['zyte']['api_key']}:@proxy.crawlera.com:8011/",
                    "https": f"http://{c.CONFIG['zyte']['api_key']}:@proxy.crawlera.com:8011/",
                },
                verify=os.path.join(c.ROOT_DIR, "zyte-ca.crt"),
                timeout=c.WEB_DRIVER_TIMEOUT_SECOND,
            )
            sleep(sleep_time)
            if "All download attempts failed. Please retry." not in response.text:
                break
            logging.info(f"Got zyte internal error, retrying {count} time...")
            sleep_time += 5
            count += 1
        self.html_text = response.text  # for debug
        if "All download attempts failed. Please retry." in response.text:
            raise Exception("Failed to load url by Zyte, exceeded max iteration.")
        return response.text

    # se
    def wait_until_xpath(self, xpath, driver=None):
        if not driver:
            driver = self.driver
        waiter = WebDriverWait(driver, c.WEB_DRIVER_TIMEOUT_SECOND)
        waiter.until(EC.presence_of_element_located((By.XPATH, xpath)))
        return driver.find_elements(by=By.XPATH, value=xpath)

    # se
    def wait_until_any_xpath(self, xpath1, xpath2, driver=None):
        if not driver:
            driver = self.driver
        waiter = WebDriverWait(driver, c.WEB_DRIVER_TIMEOUT_SECOND)
        waiter.until(
            lambda wd: len(wd.find_elements(By.XPATH, xpath1)) > 0
            or len(wd.find_elements(By.XPATH, xpath2)) > 0
        )
        return [
            driver.find_elements(by=By.XPATH, value=xpath1),
            driver.find_elements(by=By.XPATH, value=xpath2),
        ]

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

    # se
    def move_to_center(self, element):
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)

    def move_to_element(self, element):
        actions = ActionChains(self.driver)
        actions.move_to_element(element).perform()

    def get_substring_by_regex(self, string, regex):
        match = re.search(regex, string)
        if match:
            return match.group(1)
        return None
