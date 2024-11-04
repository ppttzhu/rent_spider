from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from fetch.fetch import Fetch


class FetchJacksonPark(Fetch):
    def fetch_web(self):
        self.get_url_with_retry(self.url)
        results_xpath = "//div[@class='availibility-box']"
        no_results_xpath = "//h2[contains(text(), 'No results found.')]"
        self.web_wait.until(
            EC.any_of(
                EC.presence_of_element_located((By.XPATH, results_xpath)),
                EC.presence_of_element_located((By.XPATH, no_results_xpath)),
            )
        )
        if self.driver.find_elements(by=By.XPATH, value=no_results_xpath):
            return
        room_list = self.driver.find_elements(by=By.XPATH, value=results_xpath)
        for room in room_list:
            room_soup = BeautifulSoup(room.get_attribute("innerHTML"), "html.parser")
            building_name = room_soup.find("div", {"class": "tower-title ng-binding"})
            building_name = building_name.text.replace(" Jackson Park", "JP")
            room_number = room_soup.find("div", {"class": "box-title ng-binding"})
            room_number = (
                room_number.text.replace("Residence", "")
                .replace("\n", "")
                .replace(" ", "")
            )
            property_detail = room_soup.find_all(
                "div", {"class": "property-details ng-binding"}
            )
            self.add_room_info(
                room_number=f"{room_number} - {building_name}",
                room_type=property_detail[0].text,
                move_in_date="-",
                room_price=property_detail[1].text,
            )

    def process_room_type(self, room_type):
        if "studio" in room_type.lower():
            return "0Studio"
        return (
            room_type.replace("Bedroom", "B")
            .replace("Bathroom", "B")
            .replace("\n", "")
            .replace("/", "")
            .replace(" ", "")
        )
