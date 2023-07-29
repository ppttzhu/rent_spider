from fetch.fetchStreetEasy import FetchStreetEasy


class FetchJacksonParkAWS(FetchStreetEasy):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.table_class = "nice_table listings building-pages active-rentals-table"

    def process_room_number(self, room_number):
        building_alias = ""
        if "28-40" in room_number:
            building_alias = "1JP"
        elif "28-30" in room_number:
            building_alias = "2JP"
        elif "28-10" in room_number:
            building_alias = "3JP"
        # Gotham Point
        elif "1-15 57th Avenue" in room_number:
            building_alias = "North Tower"
        elif "56-27 2nd Street" in room_number:
            building_alias = "South Tower"
        room_number = room_number.split(" - ")[0].replace("#", "").replace("\n", "")
        return f"{room_number} - {building_alias}"
