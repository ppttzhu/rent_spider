import logging
from time import sleep

from selenium.webdriver.common.by import By

from fetch.fetch import Fetch


class FetchIronState(Fetch):
    def __init__(self, driver, browser):
        super().__init__(driver, browser)
        self.room_type_map = [
            ("^Studio, 1 Bathroom$", "Studio"),
            ("^1Bedroom, 1 Bathroom$", "1B1B"),
            ("^2Bedroom, 2 Bathroom$", "2B2B"),
            ("^3Bedroom, 2 Bathroom$", "3B2B"),
        ]

    def fetch_web(self):
        self.get_url_with_retry(self.url)
        [empty_text, links] = self.wait_until_any_xpath(
            '//div[@class="message-not-result"]',
            '//article[contains(@class, "floorplans-box")]/a',
        )
        if empty_text:
            logging.info(f"No room available in {self.website_name}, skipping...")
            return
        detail_hrefs = []
        for link in links:
            detail_hrefs.append(link.get_attribute("href"))
        for href in detail_hrefs:
            self.fetch_room_info(href)

    def fetch_room_info(self, href):
        self.get_url_with_retry(href)
        rooms = self.wait_until_xpath('//article[contains(@class, "property-box")]/a/div')
        for room in rooms:
            self.move_to_center(room)
            sleep(2)
            move_in_date = room.find_element(by=By.XPATH, value=".//ul[1]/li").text.replace(
                "AVAILABLE", ""
            )
            room_price = room.find_element(by=By.XPATH, value=".//ul[2]/li[1]").text
            room_type = room.find_element(by=By.XPATH, value=".//ul[2]/li[3]").text
            room_number = room.find_element(by=By.XPATH, value=".//h3").text.replace("Unit ", "")
            self.add_room_info(
                room_number=room_number,
                room_type=room_type,
                move_in_date=move_in_date,
                room_price=room_price,
                room_url=href,
            )
