from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from fetch.fetch import Fetch


class FetchUrby(Fetch):

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
        try:
            self.fetch_rooms_info()
        except Exception:
            self.close_popup()
            self.fetch_rooms_info()

    def fetch_rooms_info(self):
        rooms = self.wait_until_xpath("//a[@class='floorplan-card-link']")
        for room in rooms:
            self.move_to_center(room)
            unit_details = room.find_element_by_xpath(".//div[@class='unit-details']").text.replace(
                "\n", ""
            )
            room_number = self.get_substring_by_regex(unit_details, r"Apt. (\d+)")
            bedroom = self.get_substring_by_regex(unit_details, r"(\d) Bed")
            bathroom = self.get_substring_by_regex(unit_details, r"(\d) Bath")
            room_type = f"{bedroom}B{bathroom}B" if int(bedroom) > 0 else "Studio"

            move_in_date = room.find_element_by_xpath(
                ".//div[contains(@class, 'availab')]"
            ).get_attribute("textContent")
            move_in_date = (
                move_in_date
                if move_in_date == "Available Now"
                else move_in_date.replace("Available ", "")
            )

            room_price = room.find_element_by_xpath(".//span[@class='price-number']").text
            self.add_room_info(
                room_number,
                room_type,
                move_in_date,
                room_price,
                room.get_attribute("href"),
            )
