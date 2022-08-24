from bs4 import BeautifulSoup

from fetch.fetchStreetEasy import FetchStreetEasy


class FetchJacksonAve(FetchStreetEasy):
    def fetch_room_info(self, room):
        html_doc = self.get_html_doc(room["room_href"])
        self.check_blocked(html_doc)
        soup = BeautifulSoup(html_doc, "html.parser")
        move_in_date = soup.find("div", {"class": "Vitals-data"})
        net_price = soup.find(
            "p", {"class": "Text-sc-1xyuphd-0 styled__DetailText-odgkne-2 lmNDzS"}
        )
        room_price = room["room_price"]
        if net_price:
            room_price = f"{net_price.text.split()[0]} Net {room_price} Gross"
        self.add_room_info(
            room_number=room["room_number"],
            room_type=room["room_type"],
            move_in_date=move_in_date.text,
            room_price=room_price,
        )
