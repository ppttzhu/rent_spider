from collections import defaultdict
from time import sleep

from selenium.webdriver.common.by import By

from fetch.fetch import Fetch


class FetchVeris(Fetch):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.room_type_map = [
            ("^Studio / 1 Bath$", "Studio"),
            ("^1 Bed / 1 Bath$", "1B1B"),
            ("^2 Beds / 1 Bath$", "2B1B"),
            ("^2 Beds / 2 Bath$", "2B2B"),
            ("^2 Beds / 2.5 Bath$", "2B2.5B"),
            ("^3 Beds / 2 Bath$", "3B2B"),
        ]

    def slow_button_click(self, button):
        try:
            self.move_to_center(button)
            sleep(3)
            button.click()
        except Exception:
            self.driver.switch_to.frame("webchat-iframe")
            webchat_close = self.driver.find_elements(
                by=By.XPATH,
                value='//webchat[@class="ng-star-inserted"]/header/nav',
            )
            webchat_close[0].click()
            self.driver.switch_to.default_content()
            button.click()

    def fetch_web(self):
        self.get_url_with_retry(self.url)
        rooms_dict = defaultdict(dict)
        cur_page = 1
        while True:
            rooms = self.wait_until_xpath("//div[@class='omg-results-card bg-white']")
            for room in rooms:
                room_info = room.find_elements(
                    by=By.XPATH,
                    value='.//div[contains(@class, "omg-results-card-body-element px-4")]',
                )
                self.add_room_info(
                    room_number=room_info[1].text,
                    room_type=room_info[2].text,
                    room_price=room_info[3].text.replace("From ", ""),
                    move_in_date=room_info[4].text.split("\n")[0],
                )
            cur_page += 1
            try:
                next_page_button = self.driver.find_element(
                    by=By.XPATH,
                    value=f'//span[@data-page="{cur_page-1}" and text()="{cur_page}"]',
                )
            except Exception:
                break
            self.slow_button_click(next_page_button)
            sleep(3)
        for room in rooms_dict.values():
            if room.get("room_number") is None:
                continue  # some room does not exist in floor plan view, skip them
            self.add_room_info(**room)
