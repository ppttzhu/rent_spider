import json
import logging
import re
from datetime import datetime

from bs4 import BeautifulSoup

from fetch.fetch import Fetch


class FetchStreetEasy(Fetch):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.table_class = "nice_table building-pages BuildingUnit-table"
        self.new_ui = False

    def fetch_web(self):
        html_doc = self.get_html_doc(self.url)
        self.check_blocked(html_doc)
        soup = BeautifulSoup(html_doc, "html.parser")
        script = soup.find("script", {"id": "__NEXT_DATA__"})
        if script:
            self.new_ui = True
            self.fetch_new_ui(script)
        table = soup.find_all("table", {"class": self.table_class})
        self.fetch_old_ui(table)

    def fetch_new_ui(self, script):
        data = json.loads(script.string)
        all_rooms = data["props"]["pageProps"]["building"]["rentalInventorySummary"][
            "availableListingDigests"
        ]
        filtered_rooms = [room for room in all_rooms if room["noFee"] and room["status"] == "OPEN"]
        for room in filtered_rooms:
            self.add_room_info(
                room_number=room["unit"],
                room_type=self.get_room_type(room),
                move_in_date=self.get_move_in_date(room),
                room_price=self.get_room_price(room),
                room_url=room.get("quickUrl") or room.get("url"),
            )

    def get_room_type(self, room):
        bed_count = room["bedroomCount"]
        if bed_count == 0:
            return "0Studio"
        bath_count = str(room["fullBathroomCount"])
        if room["halfBathroomCount"] > 0:  # not likely to be larger than 1
            bath_count += ".5"
        return f"{bed_count}B{bath_count}B"

    def get_room_price(self, room):
        price = room["price"]
        months_free = room["monthsFree"]
        if months_free:
            lease_term = room["leaseTerm"]
            net_price = round(price * (lease_term - months_free) / lease_term)
            return f"N${net_price} G${price} {months_free}/{lease_term}"
        return str(price)

    def get_move_in_date(self, room):
        move_in_date = room["availableAt"]
        date_format = "%Y-%m-%d"
        move_in_date_obj = datetime.strptime(move_in_date, date_format)
        return (
            move_in_date_obj.strftime("%m/%d/%Y")
            if move_in_date_obj > datetime.now()
            else "Available Now"
        )

    def fetch_old_ui(self, table):
        if not table:
            logging.info(f"No room available in {self.website_name}, skipping...")
            return
        rows = table[-1].find("tbody").find_all("tr")
        rooms = []
        for row in rows:
            if "no fee" not in row.text.lower():
                continue
            room = row.find_all("td")
            rooms.append(
                {
                    "room_href": room[0].find("a", href=True)["href"],
                    "room_number": room[0].text,
                    "room_type": room[2].text + room[3].text,
                    "room_price": room[1].text.split()[0],
                }
            )
        for room in rooms:
            self.fetch_room_info(room)

    def fetch_room_info(self, room):
        room_url = room["room_href"]
        html_doc = self.get_html_doc(room_url)
        self.check_blocked(html_doc)
        soup = BeautifulSoup(html_doc, "html.parser")
        move_in_date = soup.find("div", {"class": "Vitals-data"})
        room_price = room["room_price"]
        if "netEffectivePrice" in html_doc:
            info = re.findall(r"\{.*?netEffectivePrice.*?\}", html_doc)[0].replace(
                '{"rentalData":', ""
            )
            info = json.loads(info)
            net_price = info["netEffectivePrice"]
            free_month = round(info["freeMonths"])
            total_month = round(info["leaseTerm"])
            room_price = f'N{net_price} G{room["room_price"]} {free_month}/{total_month}'
        self.add_room_info(
            room_number=room["room_number"],
            room_type=room["room_type"],
            move_in_date=move_in_date.text,
            room_price=room_price,
            room_url=room_url,
        )

    def process_room_number(self, room_number):
        return room_number.split(" - ")[0].replace("#", "").replace("\n", "").replace("-", "")

    def process_room_type(self, room_type):
        if self.new_ui:
            return room_type
        if "studio" in room_type:
            return "0Studio"
        bed_index = room_type.find("bed")
        if bed_index == -1:
            return "0Studio"
        bed_count = int(room_type[bed_index - 2])
        bath_index = room_type.find("bath")
        bath_count = int(room_type[bath_index - 2])
        return f"{bed_count}B{bath_count}B"

    def check_blocked(self, doc):
        if "Pardon Our Interruption" in doc:
            raise Exception("We are blocked")
