import logging

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from fetch.fetch import Fetch


class FetchHeatherwood(Fetch):
    def fetch_web(self):
        self.get_url_with_retry(self.url)
        if self.check_availability():
            logging.info(f"No room available in {self.website_name}, skipping...")
            return

        room_info = []
        rooms = self.wait_until_xpath('//div[@class="fp-card"]')
        for room in rooms:
            apply_button = room.find_element_by_xpath('.//div[@class="fp-button"]')
            room_url = self.find_href_in_inner_html(apply_button.get_attribute("innerHTML"))
            if room_url:
                room_type = room.find_element_by_xpath('//span[@class="fp-type"]').text
                room_info.append({"room_type": room_type, "url": room_url})
        for room in room_info:
            self.fetch_room(room)

    def fetch_room(self, room):
        self.get_url_with_retry(room["url"])
        self.web_wait.until(EC.presence_of_element_located((By.XPATH, "//table/tbody/tr")))
        room_list = self.driver.find_elements(by=By.XPATH, value="//table/tbody/tr")
        for room_idx in range(len(room_list)):
            room_number = self.web_wait.until(
                EC.presence_of_element_located(
                    (By.XPATH, f'//td[@data-selenium-id="Apt{str(room_idx + 1)}"]')
                )
            ).text
            # Go to Order Page
            current_url = self.driver.current_url
            self.web_wait.until(
                EC.presence_of_element_located(
                    (By.XPATH, '//input[contains(@class, "UnitSelect")]')
                )
            ).click()
            self.driver.switch_to.window(self.driver.window_handles[0])
            move_in_date = self.web_wait.until(
                EC.presence_of_element_located((By.ID, "sMoveInDate"))
            ).get_attribute("value")
            room_price = self.wait_until_xpath('//div[@id="divPricingInfo"]/div/div/label')[-1].text
            self.add_room_info(
                room_number=room_number,
                room_type=room["room_type"],
                move_in_date=move_in_date,
                room_price=room_price,
            )
            self.get_url_with_retry(current_url)
            self.driver.switch_to.window(self.driver.window_handles[0])

    def check_availability(self):
        unavailable_text = self.driver.find_elements(
            by=By.XPATH, value='//p[contains(text(),"not available")]'
        )
        return len(unavailable_text) > 0

    def process_room_type(self, room_type):
        if "studio" in room_type.lower():
            return "0Studio"
        return (
            room_type.replace("Beds", "B")
            .replace("Baths", "B")
            .replace("Bed", "B")
            .replace("Bath", "B")
            .replace("-", "")
            .replace(" ", "")
        )

    def find_href_in_inner_html(self, inner_html):
        try:
            start_index = inner_html.index("href") + 6
            end_index = start_index
            while inner_html[end_index] != '"':
                end_index += 1
            return inner_html[start_index:end_index]
        except Exception:
            return None
