import json

from selenium.webdriver.common.by import By

from fetch.fetch import Fetch
from utils.utils import find_closing_bracket


class FetchAvaFortGreene(Fetch):
    def fetch_web(self):
        self.get_url_with_retry(self.url)
        scripts = self.driver.find_elements(by=By.XPATH, value='.//script[@id="fusion-metadata"]')
        script_text = scripts[0].get_attribute("innerHTML")
        start_index = script_text.find('"units"') + 8
        end_index = find_closing_bracket(script_text, start_index)
        rooms = json.loads(script_text[start_index : end_index + 1])
        for room in rooms:
            # Process price
            if room.get("lowestPricePerMoveInDate"):
                price = room.get("lowestPricePerMoveInDate")
                gross_price, net_price = price["price"], price["netEffectivePrice"]
            elif room.get("pricesPerMoveinDate"):
                gross_price, net_price = 999999, 999999
                for price in room["pricesPerMoveinDate"]:
                    for price1 in price["pricesPerTerms"].values():
                        if price1["netEffectivePrice"] < net_price:
                            gross_price = price1["price"]
                            net_price = price1["netEffectivePrice"]
            final_price = f"${net_price}"
            if net_price != gross_price:
                final_price = f"N${net_price} G${gross_price}"

            # Process room type
            bedroom = room["bedroom"]
            bathroom = room["bathroom"]
            room_type = f"{bedroom}B{bathroom}B"
            if bedroom == 0:
                room_type = "Studio"

            # Process room url
            room_unit_id = room["unitId"].split("-")
            room_url_suffix = "-".join([room_unit_id[1]] + room_unit_id[1:])
            room_url = f"{self.url}/apartment/{room_url_suffix}"

            self.add_room_info(
                room_number=room["name"],
                room_type=room_type,
                move_in_date=room["availableDate"].split(" ")[0],
                room_price=final_price,
                room_url=room_url,
            )
