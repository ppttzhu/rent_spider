import logging

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from fetch.fetch import Fetch


class Fetch981Management(Fetch):
    def fetch_web(self):
        self.get_url_with_retry(self.url)
        if self.check_availability():
            logging.info(f"No room available in {self.website_name}, skipping...")
            return
        room_types_elements = self.wait_until_xpath("//a[contains(@id, 'uiTab')]")

        room_types = [
            (index, element.accessible_name) for index, element in enumerate(room_types_elements)
        ]
        for index, room_type in room_types:
            self.fetch_room_info(room_type, index)

    def fetch_room_info(self, room_type, index):
        self.driver.find_element_by_id(f"uiTab{index}").click()
        apply_button = self.web_wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, f'//div[@id="collapse-tab{str(index)}"]/div/div[3]/a')
            )
        )
        if "contact us" in apply_button.text.lower():
            return
        apply_button.click()
        self.driver.switch_to.window(self.driver.window_handles[0])
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
                    (By.XPATH, f'//button[@data-selenium-id="Select_{str(room_idx + 1)}"]')
                )
            ).click()
            self.driver.switch_to.window(self.driver.window_handles[0])
            move_in_date = self.web_wait.until(
                EC.presence_of_element_located((By.ID, "sMoveInDate"))
            ).get_attribute("value")
            room_price = self.web_wait.until(
                EC.presence_of_element_located(
                    (By.XPATH, '//div[@id="divPricingInfo"]/div/div[2]/label')
                )
            ).text
            self.add_room_info(
                room_number=room_number,
                room_type=room_type,
                move_in_date=move_in_date,
                room_price=room_price,
            )
            self.get_url_with_retry(current_url)
            self.driver.switch_to.window(self.driver.window_handles[0])
        self.get_url_with_retry(self.url)
        self.driver.switch_to.window(self.driver.window_handles[0])

    def check_availability(self):
        unavailable_text = self.driver.find_elements(
            by=By.XPATH, value='//p[contains(text(),"not available")]'
        )
        return len(unavailable_text) > 0
