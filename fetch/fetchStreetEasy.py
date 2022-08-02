import logging
import re
from random import randrange
from time import sleep

from bs4 import BeautifulSoup

from fetch.fetch import Fetch


class FetchStreetEasy(Fetch):
    def __init__(self, driver, browser):
        super().__init__(driver, browser)
        self.page = self.browser.new_page()
        self.timeout = 5
        # don't load image and avoid doubleclick request
        self.page.route(
            re.compile(r"(\.png$)|(\.jpg$)|(\.webp$)|(doubleclick)"), lambda route: route.abort()
        )

    def fetch_web(self):
        html_doc = self.get_html_doc()
        self.check_blocked(html_doc)
        soup = BeautifulSoup(html_doc, "html.parser")
        table = soup.find_all("table", {"class": "nice_table building-pages BuildingUnit-table"})
        rows = table[-1].find_all("tr", {"class": "BuildingUnit-table BuildingUnit-table--row"})
        rooms = []
        for row in rows:
            if "no fee" not in row.text.lower():
                continue
            room = row.find_all("td")
            rooms.append(
                {
                    "room_number": room[0].text.split(" - ")[0].replace("#", "").replace("\n", ""),
                    "room_type": room[2].text + room[3].text,
                    "room_price": room[1].text.split()[0],
                }
            )
        for room in rooms:
            self.fetch_room_info(room)

    def fetch_room_info(self, room):
        sleep_time = randrange(15, 25)
        logging.info(f"Sleep {sleep_time}s to avoid being blocked...")
        sleep(sleep_time)
        html_doc = self.get_html_doc_room(room["room_number"])
        self.check_blocked(html_doc)
        soup = BeautifulSoup(html_doc, "html.parser")
        move_in_date = soup.find("div", {"class": "Vitals-data"})
        self.add_room_info(
            room_number=room["room_number"],
            room_type=room["room_type"],
            move_in_date=move_in_date.text,
            room_price=room["room_price"],
        )

    def get_html_doc(self):
        logging.info(f"Loading {self.url}...")
        self.page.goto(self.url, wait_until="domcontentloaded", timeout=self.timeout * 60 * 1000)
        return self.page.content()

    def get_html_doc_room(self, room_number):
        logging.info(f"Loading {self.url}/{room_number}...")
        self.page.goto(
            f"{self.url}/{room_number}",
            wait_until="domcontentloaded",
            timeout=self.timeout * 60 * 1000,
        )
        return self.page.content()

    def process_room_type(self, room_type):
        if "studio" in room_type:
            return "0Studio"
        bed_index = room_type.find("bed")
        bed_count = int(room_type[bed_index - 2])
        bath_index = room_type.find("bath")
        bath_count = int(room_type[bath_index - 2])
        return f"{bed_count}B{bath_count}B"

    def check_blocked(self, doc):
        if "Pardon Our Interruption" in doc:
            raise Exception("We are blocked")
