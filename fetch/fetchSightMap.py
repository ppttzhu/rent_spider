import json

import requests

import constants as c
from fetch.fetch import Fetch


class FetchSightMap(Fetch):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.api_url = ""  # override in child class

    def fetch_web(self):
        response = requests.get(
            self.api_url,
            timeout=c.WEB_DRIVER_TIMEOUT_SECOND,
        )

        floor_plans = json.loads(response.text)["data"]["floor_plans"]
        floor_plans_dict = {}
        for floor_plan in floor_plans:
            bedroom = floor_plan["bedroom_count"]
            bathroom = floor_plan["bathroom_count"]
            room_type = f"{bedroom}B{bathroom}B"
            if bedroom == 0:
                room_type = "Studio"
            floor_plans_dict[floor_plan["id"]] = room_type

        rooms = json.loads(response.text)["data"]["units"]
        for room in rooms:
            room_type = floor_plans_dict[room["floor_plan_id"]]
            move_in_date = room["available_on"]
            if room["display_available_on"] == "Available Now":
                move_in_date = room["display_available_on"]
            else:
                available_on = room["available_on"].split("-")
                move_in_date = "/".join([available_on[1], available_on[2], available_on[0]])

            self.add_room_info(
                room_number=room["unit_number"],
                room_type=room_type,
                move_in_date=move_in_date,
                room_price=room["display_price"],
                room_url=self.get_room_url(room),
            )

    def get_room_url(self, room):
        raise NotImplementedError("Must override abstract method")
