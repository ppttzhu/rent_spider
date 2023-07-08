import json
import logging
import re

from bs4 import BeautifulSoup

from fetch.fetch import Fetch


class FetchStreetEasy(Fetch):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.table_class = "nice_table building-pages BuildingUnit-table"

    def fetch_web(self):
        html_doc = self.get_html_doc_with_zyte(self.url)
        self.check_blocked(html_doc)
        soup = BeautifulSoup(html_doc, "html.parser")
        table = soup.find_all("table", {"class": self.table_class})
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
        html_doc = self.get_html_doc_with_zyte(room_url)
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
