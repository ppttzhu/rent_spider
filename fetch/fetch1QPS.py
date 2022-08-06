from fetch.fetchStreetEasy import FetchStreetEasy


class Fetch1QPS(FetchStreetEasy):
    def get_room_url(self, room_number):
        room_number = (
            room_number.split(" - ")[0].replace("#", "").replace("\n", "").lower().zfill(4)
        )
        return f"{self.url}/{room_number}"
