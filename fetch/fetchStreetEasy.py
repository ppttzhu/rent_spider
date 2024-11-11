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

        # see if show more button exist
        show_more_button_class = "eevXss"
        if soup.find_all("button", {"class": re.compile(f".*{show_more_button_class}.*")}):
            # click show more button
            updated_html = self.get_html_doc_with_actions(self.url, [
                {
                    "action": "click",
                    "selector": {
                        "type": "xpath",
                        "value": f".//button[contains(@class, '{show_more_button_class}')]"
                    }
                },
            ])
            if updated_html:
                soup = BeautifulSoup(updated_html, "html.parser")

        panel = soup.find_all("div", {"id": self.panel_id})
        self.fetch_new_ui(panel)
        table = soup.find_all("table", {"class": self.table_class})
        self.fetch_old_ui(table)

    def fetch_new_ui(self, panel):
        if not panel:
            logging.info(f"No room available in new {self.website_name}, skipping...")
            return
        rows = panel[-1].find_all("div", {"data-testid": "inventory-card-component"})
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
            room_price = row.find("p", {"class": re.compile(f".*ikBOAQ.*")}).text
            if "month lease" in row.text.lower():
                gross_price = round(float(room_price.replace("$", "").replace(",","")))
                months = row.find_all("p", {"class": re.compile(f".*hvszxm.*")})
                free_month = float(months[0].text.split(" ")[0])
                total_month = float(months[1].text.split("-")[0])
                net_price = round(gross_price/total_month*(total_month-free_month))
                room_price = (
                    f'N{net_price} G{gross_price} {free_month}/{total_month}'
                )
            move_in_date = row.find("div", {"data-testid": "listingLabel-availability"}).find("span")

            self.add_room_info(
                room_number=room_href.text,
                room_type=bed_count + bath_count,
                move_in_date=move_in_date.text,
                room_price=room_price,
                room_url=room_href["href"],
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
        if "Effective Rent" in html_doc:
            price_details = soup.find("div", {"data-se-component": "rentalPricesAndTerms"}).find_all("li")
            net_price = price_details[0].text.split(" ")[0]
            free_month = round(float(price_details[1].text.split(" ")[0]))
            total_month = round(float(price_details[2].text.split("-")[0]))
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

    def check_blocked(self, doc):
        if "Pardon Our Interruption" in doc:
            raise Exception("We are blocked")
