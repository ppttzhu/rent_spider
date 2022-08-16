from bs4 import BeautifulSoup

from fetch.fetch import Fetch


class FetchJacksonPark(Fetch):
    def __init__(self, driver, browser):
        super().__init__(driver, browser)
        self.init_page()

    def fetch_web(self):
        html_doc = self.get_html_doc(self.url, "networkidle")
        soup = BeautifulSoup(html_doc, "html.parser")
        room_list = soup.find_all("div", {"class": "availibility-box"})
        for room in room_list:
            building_name = room.find("div", {"class": "tower-title ng-binding"})
            building_name = building_name.text.replace(" Jackson Park", "JP")
            room_number = room.find("div", {"class": "box-title ng-binding"})
            room_number = room_number.text.replace("Residence", "").replace("\n", "")
            property_detail = room.find_all("div", {"class": "property-details ng-binding"})
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
        )
