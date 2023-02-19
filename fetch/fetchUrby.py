from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from fetch.fetch import Fetch


class FetchUrby(Fetch):
    def __init__(self, driver, browser):
        super().__init__(driver, browser)
        self.room_type_map = [
            ("^0 Bed, 1 Bath$", "Studio"),
            ("^1 Bed, 1 Bath$", "1B1B"),
            ("^2 Beds, 1 Bath$", "2B1B"),
            ("^2 Beds, 2 Bath$", "2B2B"),
            ("^3 Beds, 2 Bath$", "3B2B"),
        ]

    def close_popup(self):
        try:
            xpath = "//div[@class='scroll-container']"
            waiter = WebDriverWait(self.driver, 3)
            waiter.until(EC.presence_of_element_located((By.XPATH, xpath)))
            ad_container = self.driver.find_elements(by=By.XPATH, value=xpath)[0]
            ad_container.find_element_by_xpath(".//a[@class='close']").click()
        except Exception:
            print("Did not find close button, skipping")

    def fetch_web(self):
        self.get_url_with_retry(self.url)
        self.close_popup()
        while True:
            try:
                self.fetch_rooms_info()
            except Exception:
                self.close_popup()
                self.fetch_rooms_info()
            pagination = self.driver.find_element_by_xpath('//div[@class="pagination"]')
            next_page_button = pagination.find_element_by_xpath(".//button[2]")
            if not next_page_button.is_enabled():
                break
            try:
                next_page_button.click()
            except Exception:
                self.close_popup()
                next_page_button.click()

    def fetch_rooms_info(self):
        rooms = self.wait_until_xpath("//article[@class='card']")
        for room in rooms:
            self.move_to_center(room)
            room_number = room.find_element_by_xpath(".//p[contains(@class, 'unit')]").text
            room_type = room.find_element_by_xpath(".//p[contains(@class, 'beds-baths')]").text
            move_in_date = room.find_element_by_xpath(
                ".//p[contains(@class, 'ribbon')]"
            ).text.replace("Available ", "")
            room_price = room.find_element_by_xpath(".//p[contains(@class, 'price')]").text.replace(
                "/MO", ""
            )
            room_url = room.find_element_by_xpath(".//a[contains(@class, 'image')]").get_attribute(
                "href"
            )
            self.add_room_info(
                room_number,
                room_type,
                move_in_date,
                room_price,
                room_url,
            )
