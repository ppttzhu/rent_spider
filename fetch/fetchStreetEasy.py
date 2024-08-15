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
        self.panel_id = "available-units-simple-tabpanel-0"

    def fetch_web(self):
        html_doc = self.get_html_doc(self.url)
        soup = BeautifulSoup(html_doc, "html.parser")
        panel = soup.find_all("div", {"id": self.panel_id})
        self.fetch_new_ui(panel)
        table = soup.find_all("table", {"class": self.table_class})
        self.fetch_old_ui(table)

    def fetch_new_ui(self, panel):
        if not panel:
            logging.info(f"No room available in new {self.website_name}, skipping...")
            return
        rows = panel[-1].find_all("div", {"data-testid": "inventory-card-component"})
        rooms = []
        for row in rows:
            if "no fee" not in row.text.lower():
                continue
            room_href = row.find("a", href=True)
            room_types = row.find(
                "div", {"data-testid": "listing-description-icons"}
            ).find_all("p", {"class": "Caption_base_GEtMu"})
            bed_count = (
                room_types[0]
                .text.replace("beds", "B")
                .replace("bed", "B")
                .replace(" ", "")
            )
            bath_count = (
                room_types[1]
                .text.replace("baths", "B")
                .replace("bath", "B")
                .replace(" ", "")
            )
            room_price = row.find("p", {"class": re.compile(f".*ikBOAQ.*")})
            rooms.append(
                {
                    "room_href": room_href["href"],
                    "room_number": room_href.text,
                    "room_type": bed_count + bath_count,
                    "room_price": room_price.text,
                }
            )
        for room in rooms:
            self.fetch_room_info(room)

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
            logging.info(f"No room available in old {self.website_name}, skipping...")
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
            room_price = (
                f'N{net_price} G{room["room_price"]} {free_month}/{total_month}'
            )
        self.add_room_info(
            room_number=room["room_number"],
            room_type=room["room_type"],
            move_in_date=move_in_date.text,
            room_price=room_price,
            room_url=room_url,
        )

    def process_room_number(self, room_number):
        return (
            room_number.split(" - ")[0]
            .replace("#", "")
            .replace("\n", "")
            .replace("-", "")
        )

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
