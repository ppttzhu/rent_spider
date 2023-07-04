from collections import defaultdict
from time import sleep

from selenium.webdriver.common.by import By

from fetch.fetch import Fetch


class FetchVYV(Fetch):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.room_type_map = [
            ("^Studio / 1 Bath$", "Studio"),
            ("^1 Bed / 1 Bath$", "1B1B"),
            ("^1 Bed / 1 Bath.*Den$", "1B1BD"),
            ("^2 Bed / 1 Bath$", "2B1B"),
            ("^2 Bed / 2 Bath$", "2B2B"),
            ("^3 Bed / 2 Bath$", "3B2B"),
        ]

    def fetch_web(self):
        self.get_url_with_retry(self.url)
        list_view_button = self.wait_until_xpath(
            '//span[@class="fl-button-text" and text()="List View"]'
        )[0]
        self.move_to_center(list_view_button)
        list_view_button.click()
        self.fetch_room()

        # fetch north tower
        north_tower_button = self.driver.find_element_by_xpath(
            '//button[@class="floorplan-tower-button" and @data-id="North"]'
        )
        self.move_to_center(north_tower_button)
        north_tower_button.click()
        sleep(1)
        self.fetch_room()

    def fetch_room(self):
        rooms = self.wait_until_xpath('//div[@class="floorplan-item"]')
        print(rooms)
        for room in rooms:
            room_number = room.find_element_by_xpath(
                './/div[contains(@class, "floorplan-name")]'
            ).text
            room_type = room.find_element_by_xpath(
                './/div[contains(@class, "bed-bath-count")]'
            ).text
            room_price = room.find_element_by_xpath(
                './/div[contains(@class, "floorplan-rent-range")]'
            ).text
            self.add_room_info(
                room_number=room_number,
                room_type=room_type,
                move_in_date="-",
                room_price=room_price,
            )
