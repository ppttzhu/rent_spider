from time import sleep

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from fetch.fetch import Fetch


class FetchJsq(Fetch):
    def __init__(self, driver, browser):
        super().__init__(driver,  browser)
        self.room_type_map = [
            ("^One Bed/ One Bath - .*$", "1B1B"),
            ("^One Bed/ One Bath/ Plus - .*$", "1B1BD"),
            ("^Studio - .*$", "Studio"),
            ("^Two Bed/ Two Bath - .*$", "2B2B"),
            ("^Three Bed/ Two Bath - .*$", "3B2B"),
        ]

    def fetch_web(self):
        self.driver.get(self.url)
        sleep(5)  # sleep because table might not fully loaded
        self.web_wait.until(
            EC.presence_of_element_located((By.XPATH, '//table[@id="table"]/tbody/tr'))
        )
        room_list = self.driver.find_elements(by=By.XPATH, value='//table[@id="table"]/tbody/tr')
        for row in room_list:
            if not row.text:
                # FIXME: more room will show after click GO, this might not be stable
                continue
            room = row.find_elements(by=By.XPATH, value=".//td")
            self.add_room_info(
                room_number=room[1].text,
                room_type=room[2].text,
                move_in_date=room[5].text,
                room_price=room[3].text,
            )
