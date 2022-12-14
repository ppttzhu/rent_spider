from collections import defaultdict
from time import sleep

from selenium.webdriver.common.by import By

from fetch.fetch import Fetch


class FetchVeris(Fetch):
    def __init__(self, driver, browser):
        super().__init__(driver, browser)
        self.room_type_map = [
            ("^Studio / 1 Bath$", "Studio"),
            ("^1 Bed / 1 Bath$", "1B1B"),
            ("^2 Beds / 1 Bath$", "2B1B"),
            ("^2 Beds / 2 Bath$", "2B2B"),
            ("^2 Beds / 2.5 Bath$", "2B2.5B"),
            ("^3 Beds / 2 Bath$", "3B2B"),
        ]

    def fetch_web(self):
        def read_list():
            if not self.reading_list:
                self.move_to_center(view_buttons[0])
                view_buttons[0].click()
                sleep(0.5)
                self.reading_list = True
            for room in rooms:
                room_classes = room.get_attribute("class").split(" ")
                if room_classes[1] == "wpgb-card-1":
                    room_type = room.find_element(
                        by=By.XPATH, value='.//div[@class="wpgb-block-10"]'
                    ).text
                    room_price = room.find_element(
                        by=By.XPATH, value='.//div[@class="wpgb-block-8"]'
                    ).text.replace("From ", "")
                    move_in_date = room.find_element(
                        by=By.XPATH, value='.//div[@class="wpgb-block-1"]/div[1]'
                    ).text
                    rooms_dict[room_classes[2]] = {
                        **rooms_dict[room_classes[2]],
                        "room_price": room_price,
                        "room_type": room_type,
                        "move_in_date": move_in_date,
                    }

        def read_floor():
            if self.reading_list:
                self.move_to_center(view_buttons[1])
                view_buttons[1].click()
                sleep(0.5)
                self.reading_list = False
            for room in rooms:
                room_classes = room.get_attribute("class").split(" ")
                if room_classes[1] == "wpgb-card-16":
                    room_number = room.find_element(
                        by=By.XPATH, value=".//h3[contains(@class, 'wpgb-block-1')]/a[1]"
                    ).text
                    rooms_dict[room_classes[2]] = {
                        **rooms_dict[room_classes[2]],
                        "room_number": room_number,
                    }

        self.get_url_with_retry(self.url)
        rooms_dict = defaultdict(dict)
        cur_page = 1
        self.reading_list = True
        while True:
            rooms = self.wait_until_xpath("//article[contains(@class, 'wpgb-card')]")
            view_buttons = self.driver.find_elements(
                by=By.XPATH,
                value='//div[@class="uagb-button__link"]',
            )
            if self.reading_list:
                read_list()
                read_floor()
            else:
                read_floor()
                read_list()
            cur_page += 1
            try:
                next_page_button = self.driver.find_element(
                    by=By.XPATH,
                    value=f'//a[@aria-label="Goto Page {cur_page}" and @data-page="{cur_page}" and text()="{cur_page}"]',
                )
            except Exception:
                break
            self.move_to_center(next_page_button)
            next_page_button.click()
            sleep(3)
        for room in rooms_dict.values():
            self.add_room_info(**room)
