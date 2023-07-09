from time import sleep

from selenium.webdriver.common.by import By

from fetch.fetch import Fetch


class FetchDvora(Fetch):
    def fetch_web(self):
        self.get_url_with_retry(self.url)
        current_units = self.wait_until_xpath("//dvora-current-units")[0]
        self.move_to_center(current_units)
        sleep(2)
        if "No Apartments Available" in current_units.text:
            return
        room_table = self.wait_until_xpath('//tbody[@role="rowgroup"]')[0]
        rooms = room_table.find_elements(By.XPATH, ".//tr")
        for room in rooms:
            room_number = room.find_element_by_xpath(
                ".//td[contains(@class, 'cdk-column-name')]"
            ).text
            room_type = (
                room.find_element_by_xpath(".//td[contains(@class, 'cdk-column-floorplanName')]")
                .text.replace("BR", "B")
                .replace("BA", "B")
                .replace("-", "")
                .replace(" ", "")
            )
            move_in_date = room.find_element_by_xpath(
                ".//td[contains(@class, 'cdk-column-availability')]"
            ).text
            room_price = room.find_element_by_xpath(
                ".//td[contains(@class, 'cdk-column-rent')]"
            ).text
            room_url = (
                room.find_element_by_xpath(".//td[contains(@class, 'cdk-column-floorplanId')]")
                .find_element_by_xpath(".//a[contains(@class, 'md-accent')]")
                .get_attribute("href")
            )
            self.add_room_info(
                room_number=room_number,
                room_type=room_type,
                move_in_date=move_in_date,
                room_price=room_price,
                room_url=room_url,
            )
