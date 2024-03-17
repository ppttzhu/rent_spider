from fetch.fetchSightMap import FetchSightMap


class FetchLiveTheMorgan(FetchSightMap):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.api_url = "https://sightmap.com/app/api/v1/910pd727p2z/sightmaps/14497"

    def get_room_url(self, room):
        return f"https://sightmap.com/share/dgow3lqrw2m?unit_id={room['id']}"
