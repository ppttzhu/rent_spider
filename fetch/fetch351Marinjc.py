from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from fetch.fetch import Fetch


class Fetch351Marinjc(Fetch):
    def fetch_web(self):
        self.driver.get(self.url)
        self.fetch_room_info("Studio", "Studio", 0)
        self.fetch_room_info("1B1B", "1BR", 1)
        self.fetch_room_info("2B2B", "2BR", 2)

    def fetch_room_info(self, room_type, floor_plan_name, index):
        self.web_wait.until(
            EC.element_to_be_clickable((By.XPATH, f'//a[@id="uiTab{str(index)}"]'))
        ).click()
        apply_button = self.web_wait.until(
            EC.element_to_be_clickable((By.XPATH, f'//a[@data-floorplan-name="{floor_plan_name}"]'))
        )
        if "contact us" in apply_button.text.lower():
            return
        apply_button.click()
        self.driver.switch_to.window(self.driver.window_handles[0])
        self.web_wait.until(EC.presence_of_element_located((By.XPATH, "//table/tbody/tr")))
        room_list = self.driver.find_elements(by=By.XPATH, value="//table/tbody/tr")
        for row in room_list:
            room_number = row.find_element(by=By.XPATH, value='.//td[@class="td-card-name"]').text
            room_price = row.find_element(by=By.XPATH, value='.//td[@class="td-card-rent"]').text
            move_in_date = row.find_element(
                by=By.XPATH, value='.//td[@class="td-card-available"]'
            ).text
            self.add_room_info(
                room_number=room_number,
                room_type=room_type,
                move_in_date=move_in_date,
                room_price=room_price,
            )
        self.driver.get(self.url)
        self.driver.switch_to.window(self.driver.window_handles[0])
