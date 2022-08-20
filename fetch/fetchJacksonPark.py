from bs4 import BeautifulSoup

from fetch.fetch import Fetch


class FetchJacksonPark(Fetch):
    def fetch_web(self):
        self.driver.get(self.url)
        room_list = self.wait_until_xpath(self.driver, "//div[@class='availibility-box']")
        for room in room_list:
            room_soup = BeautifulSoup(room.get_attribute("innerHTML"), "html.parser")
            building_name = room_soup.find("div", {"class": "tower-title ng-binding"})
            building_name = building_name.text.replace(" Jackson Park", "JP")
            room_number = room_soup.find("div", {"class": "box-title ng-binding"})
            room_number = room_number.text.replace("Residence", "").replace("\n", "")
            property_detail = room_soup.find_all("div", {"class": "property-details ng-binding"})
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
