import re
from time import sleep

from selenium.webdriver.common.by import By

from fetch.fetch import Fetch


class FetchNewportRental(Fetch):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.max_iteration = 60
        self.building_name_priority_map = {
            "Ellipse": 1,
            "Beach": 1,
            "Aquablu": 1,
            "Revetment House": 1,
            "Laguna": 1,
            "Southampton": 2,
            "East Hampton": 2,
            "Pacific": 2,
            "Atlantic": 2,
            "Roosevelt House": 2,
            "Parkside East": 3,
            "Parkside West": 3,
            "Waterside Square North": 3,
            "Waterside Square South": 3,
            "Lincoln House": 3,
            "Riverside": 4,
        }
        self.room_type_map = [
            ("Studio", "Studio"),
            ("^1 Bedroom1 Bathroom$", "1B1B"),
            ("^2 Bedrooms1 Bathroom$", "2B1B"),
            ("^2 Bedrooms2 Bathrooms$", "2B2B"),
            ("^3 Bedrooms2 Bathrooms$", "3B2B"),
            ("^3 Bedrooms3 Bathrooms$", "3B3B"),
        ]

    def fetch_web(self):
        self.get_url_with_retry(self.url)

        # Scroll to the bottom until load all apartments
        load_more_class = ""
        count = 0
        while count < self.max_iteration and "hidden--very" not in load_more_class:
            load_more = self.wait_until_xpath('//span[text()="Load More Apartments"]/..')[0]
            load_more_class = load_more.get_attribute("class")
            self.move_to_center(load_more)
            sleep(1)
            count += 1
        if count == self.max_iteration:
            raise Exception("Failed to load all apartments, exceeded max iteration.")

        rooms = self.wait_until_xpath('//div[contains(@class, "unit-list-item")]')
        for room in rooms:
            room_url = self.base_url + room.find_element_by_xpath(
                ".//button[contains(@class, 'col-container')]"
            ).get_attribute("data-link")

            building_room_number = room.find_element_by_xpath(
                ".//div[contains(@class, 'col--01')]"
            ).text
            building_room_number_list = re.split("\||\n", building_room_number)
            building_room_number_list = [i for i in building_room_number_list if i]
            building_name = building_room_number_list[0].strip()
            room_number = building_room_number_list[1].replace("Residence", "").strip()
            merged_building_room_number = f"[{self.building_name_priority_map.get(building_name)}] {building_name} {room_number}"

            room_type = room.find_element_by_xpath(".//div[contains(@class, 'col--02')]").text
            room_type_list = re.split("\||\n", room_type)
            room_type_list = [i.strip() for i in room_type_list if i]
            room_type = "".join(room_type_list[:2])
            room_price = room.find_element_by_xpath(
                ".//span[contains(@class, 'display-price')]"
            ).text

            move_in_date = ""
            for date in room.find_elements(
                by=By.XPATH, value=".//span[contains(@class, 'unit-date-available')]"
            ):
                if date.text:
                    move_in_date = date.text
            if move_in_date != "Available Now":
                move_in_date = move_in_date.replace("Available", "").strip()

            self.add_room_info(
                room_number=merged_building_room_number,
                room_type=room_type,
                move_in_date=move_in_date,
                room_price=room_price,
                room_url=room_url,
            )
