import re

from bs4 import BeautifulSoup

from fetch.fetch981Management import Fetch981Management


class FetchHeatherwood(Fetch981Management):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.apply_button_filter = {"data-selenium-id": re.compile(".*FPButton_.*")}

    def fetch_room_info(self, room_url):
        html_doc = self.get_html_doc(room_url)
        soup = BeautifulSoup(html_doc, "html.parser")
        room_type = self.parse_room_type(soup)
        rows = self.find_all_contains(soup, "tr", "urow")
        for row in rows:
            room_number = self.parse_room_number(row)
            room_price = self.parse_room_price(row)
            move_in_date = self.parse_move_in_date(row)

            self.add_room_info(
                room_number=room_number,
                room_type=room_type,
                move_in_date=move_in_date,
                room_price=room_price,
            )

    def get_room_header(self, soup):
        return soup.find("div", {"id": re.compile(".*other-floorplans.*")}).text.lower()
