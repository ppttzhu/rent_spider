from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from fetch.fetch import Fetch


class FetchJsq(Fetch):
    def fetch_web(self):
        self.get_url_with_retry(self.url)
        self.web_wait.until(
            EC.presence_of_element_located((By.XPATH, '//div[@class="property-grid"]'))
        )
        room_list = self.driver.find_elements(
            by=By.XPATH,
            value='//div[@class="property-grid"]/article',
        )
        room_type_map = {
            "1 Bed | 1 Bath": "1B1B",
            "1 Bed + | 1 Bath": "1B1BD",
            "2 Bed | 2 Bath": "2B2B",
            "3 Bed | 2 Bath": "3B2B",
        }
        for row in room_list:
            tower = row.get_attribute("data-tower")
            room_number = row.get_attribute("data-name")
            link = row.find_element_by_xpath(".//a")
            room_type = room_type_map.get(row.get_attribute("data-floorplan"), "Studio")
            self.add_room_info(
                room_number=f"{room_number} - JD{tower[-1]}",
                room_type=room_type,
                move_in_date=row.get_attribute("data-date"),
                room_price=row.get_attribute("data-rent"),
                room_url=link.get_attribute("href"),
            )
