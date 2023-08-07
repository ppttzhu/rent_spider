import logging

from bs4 import BeautifulSoup

from fetch.fetchStreetEasy import FetchStreetEasy


class FetchSteelHaus(FetchStreetEasy):
    def fetch_web(self):
        html_doc = self.get_html_doc(self.url)
        self.check_blocked(html_doc)
        soup = BeautifulSoup(html_doc, "html.parser")
        table = soup.find_all("table", {"class": self.table_class})
        if not table:
            logging.info(f"No room available in {self.website_name}, skipping...")
            return
        rows = table[-1].find("tbody").find_all("tr")
        for row in rows:
            if "no fee" not in row.text.lower():
                continue
            room = row.find_all("td")
            self.add_room_info(
                room_number=room[0].text,
                room_type=room[2].text + room[3].text,
                move_in_date="1/1/2099",
                room_price=room[1].text.split()[0],
            )
