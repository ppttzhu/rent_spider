import json
from time import sleep

import requests

import constants as c
from fetch.fetchSightMap import FetchSightMap


class Fetch65Bay(FetchSightMap):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.api_url = "https://sightmap.com/app/api/v1/er5v5m83wny/sightmaps/6955"

    def get_room_url(self, room):
        room_leasing_price_url = room["leasing_price_url"]
        response = requests.get(
            room_leasing_price_url,
            timeout=c.WEB_DRIVER_TIMEOUT_SECOND,
        )
        sleep(0.1)
        options = json.loads(response.text)["data"]["options"]
        min_price = 10**10
        url = None
        for option in options:
            price = float(option["display_price"].replace("$", "").replace(",", ""))
            if price < min_price:
                url = option["apply_url"]
        return url
