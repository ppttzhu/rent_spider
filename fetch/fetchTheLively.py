from selenium.webdriver.common.by import By

from fetch.fetch import Fetch


class FetchTheLively(Fetch):
    def fetch_web(self):
        self.get_url_with_retry(self.url)
        floor_plans = self.wait_until_xpath('//div[@class="floor-plans"]')[0]
        rooms = floor_plans.find_elements(By.XPATH, ".//div[contains(@class, 'card ')]")
        for room in rooms:
            room_title = room.find_element_by_xpath(".//a[contains(@class, 'card__title')]")
            room_number = room_title.text
            room_url = room_title.get_attribute("href")

            room_stats = room.find_element_by_xpath(
                ".//ul[contains(@class, 'card__stats')]"
            ).find_elements(By.XPATH, ".//li")

            bedroom = room_stats[1].text.split(" ")[0]
            bathroom = room_stats[2].text.split(" ")[0].replace(".0", "")
            room_type = f"{bedroom}B{bathroom}B"
            if bedroom == "Studio":
                room_type = "Studio"
            room_price = room_stats[3].text.replace("Starting at ", "")

            move_in_date = (
                room.find_element_by_xpath(".//ul[@class='unit-list__move-in']/li")
                .text.replace("MOVE-IN ", "")
                .replace("AVAILABLE NOW", "Available Now")
            )

            self.add_room_info(
                room_number=room_number,
                room_type=room_type,
                move_in_date=move_in_date,
                room_price=room_price,
                room_url=room_url,
            )
