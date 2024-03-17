import re
from datetime import date, timedelta

from bs4 import BeautifulSoup
from dateutil import parser

from fetch.fetch import Fetch


class Fetch981Management(Fetch):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.apply_button_filter = {"href": re.compile(f".*/floorplans.*"), "name": "applynow"}

    def fetch_web(self):
        html_doc = self.get_html_doc(self.url)
        soup = BeautifulSoup(html_doc, "html.parser")
        if self.soup_check_contain(soup, "p", "not available"):
            return

        apply_buttons = soup.find_all("a", self.apply_button_filter)
        room_urls = [
            (
                self.base_url + button.attrs["href"]
                if "http" not in button.attrs["href"]
                else button.attrs["href"]
            )
            for button in apply_buttons
        ]
        for url in list(set(room_urls)):
            self.fetch_room_info(url)

    def fetch_room_info(self, room_url):
        html_doc = self.get_html_doc(room_url)
        soup = BeautifulSoup(html_doc, "html.parser")
        room_type = self.parse_room_type(soup)
        rows = self.find_all_contains(soup, "tr", "urow")
        for row in rows:
            room_number = self.parse_room_number(row)
            room_price = self.parse_room_price(row)

            button = self.find_all_contains(row, "button", "Select_")[0]
            onclick = button.attrs["onclick"]
            
            html = self.get_substring_by_regex(onclick, "href='(.*)'")
            move_in_date = self.parse_move_in_date_from_html(html)

            self.add_room_info(
                room_number=room_number,
                room_type=room_type,
                move_in_date=move_in_date,
                room_price=room_price,
                room_url=html,
            )

    def find_all_contains(self, soup, tag, text):
        return soup.find_all(tag, {"data-selenium-id": re.compile(f".*{text}.*")})

    def parse_room_price(self, soup):
        rent = self.find_all_contains(soup, "td", "Rent")[0]
        return rent.text.split(" ")[0].split("-")[0].replace("Rent:", "")

    def parse_room_number(self, soup):
        apartment = self.find_all_contains(soup, "td", "Apt")[0]
        return (
            apartment.text.replace("\n", "")
            .replace(" ", "")
            .replace("#", "")
            .replace(":", "")
            .replace("Apartment", "")
        )

    def parse_move_in_date(self, soup):
        move_in_date = self.find_all_contains(soup, "td", "AvailDate")
        if not move_in_date:
            return None
        return move_in_date[0].text

    def parse_move_in_date_from_html(self, html):
        move_in_date = ""
        move_in_date_index = html.find("MoveInDate")
        if move_in_date_index:
            for i in range(move_in_date_index + len("MoveInDate") + 1, len(html)):
                if html[i] == "&":
                    break
                move_in_date += html[i]
        tomorrow = date.today() + timedelta(days=1)
        move_in_datetime = parser.parse(move_in_date).date()
        if move_in_datetime <= tomorrow:
            return "Available Now"
        return move_in_date

    def get_room_header(self, soup):
        return soup.find("div", {"id": "available-units-container"}).text.lower()

    def parse_room_type(self, soup):
        room_header = self.get_room_header(soup)
        if "studio" in room_header:
            return "Studio"
        bedroom, bathroom = 0, 0
        for i in range(1, 5):
            if f"{i} bedroom" in room_header:
                bedroom = i
        for i in range(1, 5):
            if f"{i} bathroom" in room_header:
                bathroom = i
        return f"{bedroom}B{bathroom}B"
