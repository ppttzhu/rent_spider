import json

from selenium.webdriver.common.by import By

from fetch.fetch import Fetch
from utils.utils import find_closing_bracket


class FetchAvalon(Fetch):
    def fetch_web(self):
        self.get_url_with_retry(self.url)
        scripts = self.driver.find_elements(
            by=By.XPATH, value='.//script[@id="fusion-metadata"]'
        )
        script_text = scripts[0].get_attribute("innerHTML")
        start_index = script_text.find('"units"') + 8
        end_index = find_closing_bracket(script_text, start_index)
        rooms = json.loads(script_text[start_index : end_index + 1])
        for room in rooms:
            # Process price
            price = room["startingAtPricesUnfurnished"]["prices"]
            gross_price, net_price = price["price"], price["netEffectivePrice"]
            final_price = (
                f"N${net_price} G${gross_price}"
                if net_price != gross_price
                else f"${net_price}"
            )

            # Process room type
            bedroom = room["bedroomNumber"]
            bathroom = room["bathroomNumber"]
            room_type = f"{bedroom}B{bathroom}B"
            if bedroom == 0:
                room_type = "Studio"

            # Process room url
            room_unit_id = room["unitId"].split("-")
            room_url_suffix = "-".join([room_unit_id[1]] + room_unit_id[1:])
            room_url = f"{self.url}/apartment/{room_url_suffix}"

            # Process date
            date_string = room["startingAtPricesUnfurnished"]["moveInDate"]
            year = date_string[:4]
            month = date_string[5:7] if date_string[5] != "0" else date_string[6]
            day = date_string[8:10] if date_string[8] != "0" else date_string[9]

            self.add_room_info(
                room_number=room["unitName"],
                room_type=room_type,
                move_in_date=f"{month}/{day}/{year}",
                room_price=final_price,
                room_url=room_url,
            )
