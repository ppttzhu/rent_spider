# Deprecated

from fetch.fetchStreetEasy import FetchStreetEasy


class FetchJacksonParkAWS(FetchStreetEasy):
    def __init__(self, driver, browser):
        super().__init__(driver, browser)
        self.table_class = "nice_table listings building-pages active-rentals-table"

    def get_room_url(self, room_number):
        room_number_remove_building = (
            room_number.split(" - ")[0].replace("#", "").replace("\n", "").lower()
        )
        index = room_number.find("Jackson Avenue")
        building_number = room_number[index - 6 : index - 1].replace("-", "_")
        return f"https://streeteasy.com/building/{building_number}-jackson-avenue-long_island_city/{room_number_remove_building}"

    def process_room_number(self, room_number):
        building_alias = ""
        if "28-40" in room_number:
            building_alias = "1JP"
        elif "28-30" in room_number:
            building_alias = "2JP"
        elif "28-10" in room_number:
            building_alias = "3JP"
        room_number = room_number.split(" - ")[0].replace("#", "").replace("\n", "")
        return f"{room_number} - {building_alias}"
