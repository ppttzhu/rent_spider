from bs4 import BeautifulSoup

from fetch.fetch981Management import Fetch981Management


class FetchTheLively(Fetch981Management):
    def fetch_room_info(self, room_url):
        html_doc = self.get_html_doc(room_url)
        soup = BeautifulSoup(html_doc, "html.parser")
        room_type = self.parse_room_type(soup)
        rows = soup.find("div", {"id": "availApts"}).find_all("div", {"class": "card"})
        for row in rows:
            room_number = self.parse_room_number(row)
            room_price = self.parse_room_price(row)

            button = self.find_all_contains(row, "a", "Select_")[0]
            html = button.attrs["href"]
            move_in_date = self.parse_move_in_date_from_html(html)

            self.add_room_info(
                room_number=room_number,
                room_type=room_type,
                move_in_date=move_in_date,
                room_price=room_price,
                room_url=room_url,
            )

    def get_room_header(self, soup):
        return soup.find("h2", {"class": "h3 font-weight-normal"}).text.lower()