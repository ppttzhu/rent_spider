import logging
from time import sleep

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

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
        try:
            waiter = WebDriverWait(self.driver, 3)
            waiter.until(EC.presence_of_element_located((By.TAG_NAME, "me-chat")))
            iframe = self.driver.find_element(by=By.TAG_NAME, value="me-chat")
            script = "return arguments[0].shadowRoot"
            chat = self.driver.execute_script(script, iframe)
            exit_button = chat.find_element(
                by=By.CSS_SELECTOR, value="minimize-expand-button"
            )
            exit_button.click()
        except Exception:
            logging.warning(f"chatbot not exist, ignoring...")
        list_view_button = self.wait_until_xpath(
            '//span[@class="fl-button-text" and text()="List View"]'
        )[0]
        self.move_to_center(list_view_button)
        list_view_button.click()
        self.fetch_room()

        # fetch south tower
        south_tower_button = self.driver.find_element_by_xpath(
            '//button[@data-id="South"]'
        )
        self.move_to_center(south_tower_button)
        south_tower_button.click()
        sleep(1)
        self.fetch_room()

    def fetch_room(self):
        rooms = self.wait_until_xpath('//div[@class="floorplan-item"]')
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
