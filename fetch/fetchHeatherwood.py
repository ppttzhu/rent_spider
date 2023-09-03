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
        # TODO: change to //a|//button
        try:
            apply_buttons = self.wait_until_xpath('//a[contains(@class, "btn-viewDetails")]')
        except Exception as err:
            logging.info(f"No room available in {self.website_name}, skipping...{err}")
            return
        for index in range(len(apply_buttons)):
            self.fetch_room_info(index)

    def fetch_room_info(self, index):
        apply_button = self.wait_until_xpath(f'//a[@data-selenium-id="FPButton_{index}"]')[0]
        if "contact us" in apply_button.text.lower():
            return
        self.move_to_center(apply_button)
        apply_button.click()
        self.driver.switch_to.window(self.driver.window_handles[0])
        self.fetch_room()
        self.get_url_with_retry(self.url)
        self.driver.switch_to.window(self.driver.window_handles[0])

    def fetch_room(self):
        self.web_wait.until(EC.presence_of_element_located((By.XPATH, "//table/tbody/tr")))
        room_type = self.driver.find_elements(
            by=By.XPATH, value='//div[contains(@id,"other-floorplans")]'
        )[0].text.split("-")[-1]
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
                    (By.XPATH, f'//input[@data-selenium-id="btnUnitSelect{str(room_idx + 1)}"]')
                )
            ).click()
            self.driver.switch_to.window(self.driver.window_handles[0])
            move_in_date = self.web_wait.until(
                EC.presence_of_element_located((By.ID, "sMoveInDate"))
            ).get_attribute("value")
            room_price = self.wait_until_xpath('//div[@id="divPricingInfo"]/div/div/label')[-1].text
            self.add_room_info(
                room_number=room_number,
                room_type=room_type,
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
            room_type.replace("Bedrooms", "B")
            .replace("Bathrooms", "B")
            .replace("Bedroom", "B")
            .replace("Bathroom", "B")
            .replace(",", "")
            .replace(" ", "")
        )
