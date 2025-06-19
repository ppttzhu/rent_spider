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

        # see if show more button exist
        parse_se_js_script_error = False
        if self.has_show_more(html_doc):
            logging.info(f"Failed to parse_se_js_script for {self.website_name}")
            try:
                parsed_rooms = self.parse_se_js_script(html_doc)
            except Exception as e:
                logging.info(f"Failed to parse_se_js_script for {self.website_name}")
                parse_se_js_script_error = True
            if not parse_se_js_script_error: 
                for room in parsed_rooms:
                    self.add_room_info(**room)
        if parse_se_js_script_error: 
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
            move_in_date = row.find("div", {"data-testid": "listingLabel-availability"})
            if not move_in_date:
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
            room_price = row.find("p", {"class": re.compile(f".*sc-ae388164-5.*")}).text
            if "month lease" in row.text.lower():
                gross_price = round(float(room_price.replace("$", "").replace(",","")))
                months = row.find_all("p", {"class": re.compile(f".*hvszxm.*")})
                free_month = float(months[0].text.split(" ")[0])
                total_month = float(months[1].text.split("-")[0])
                net_price = round(gross_price/total_month*(total_month-free_month))
                room_price = (
                    f'N{net_price} G{gross_price} {free_month}/{total_month}'
                )

            self.add_room_info(
                room_number=room_href.text,
                room_type=bed_count + bath_count,
                move_in_date=move_in_date.find("span").text,
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

    def has_show_more(self, text):
        return bool(re.search(r"Show \d+ more", text))

    # code generated by chatgpt that I don't have time to clean
    def parse_se_js_script(self, html_doc):
        def extract_next_f_blocks(html):
            soup = BeautifulSoup(html, "html.parser")
            script_tags = soup.find_all("script")
            push_calls = []

            for tag in script_tags:
                if tag.string and "self.__next_f.push" in tag.string:
                    matches = re.findall(r"push\(\[(\d+),(.+?)\]\)", tag.string)
                    for index, value in matches:
                        idx = int(index)
                        value = value.strip()

                        if value in ["null", "undefined"]:
                            val = None
                        elif value.startswith('"') and value.endswith('"'):
                            try:
                                val = json.loads(value)
                            except json.JSONDecodeError:
                                val = value.strip('"')
                        else:
                            val = value  # Raw string

                        push_calls.append((idx, val))

            push_calls.sort(key=lambda x: x[0])
            return [val for _, val in push_calls if val is not None]

        def extract_json_from_text(text, start_key='{"availableRentals"'):
            start_index = text.find(start_key)
            if start_index == -1:
                raise ValueError("Start key not found")

            brace_stack = []
            in_string = False
            escaped = False
            end_index = None

            for i in range(start_index, len(text)):
                char = text[i]

                if char == '"' and not escaped:
                    in_string = not in_string

                if not in_string:
                    if char == "{":
                        brace_stack.append("{")
                    elif char == "}":
                        if brace_stack:
                            brace_stack.pop()
                            if not brace_stack:
                                end_index = i + 1
                                break

                escaped = char == "\\" and not escaped

            if end_index is None:
                raise ValueError("Could not find matching closing brace")

            json_str = text[start_index:end_index]
            return json.loads(json_str)

        def extract_room_info(listing):
            if not listing.get("noFee"):
                return
            # 1. Gross price
            gross_price = int(listing.get("price", "0").replace(",", ""))
            if listing.get("leaseTermMonths") is not None:
                total_month = int(listing.get("leaseTermMonths", 12))
                free_month = int(listing.get("monthsFree", 0))
                net_price = round(
                    gross_price / total_month * (total_month - free_month)
                )
                room_price = f"N{net_price} G{gross_price} {free_month}/{total_month}"
            else:
                room_price = gross_price

            # 3. Room number
            room_number = listing.get("unit", "").lstrip("#")

            # 4. Room type
            bedrooms = listing.get("bedrooms", "").lower()
            bathrooms = listing.get("bathrooms", "").lower()

            if "studio" in bedrooms:
                room_type = "studio"
            else:
                # Extract numbers like "2 bed" -> 2
                bed_count = re.search(r"\d+", bedrooms)
                bath_count = re.search(r"\d+", bathrooms)
                room_type = (
                    f"{bed_count.group()}B{bath_count.group() if bath_count else '?'}B"
                    if bed_count
                    else "?"
                )

            # 5. Move-in date
            move_in_date = listing.get("availabilityDate", "")

            # 6. URL
            room_url = listing.get("listingUrl", "")

            return {
                "room_number": room_number,
                "room_type": room_type,
                "move_in_date": move_in_date,
                "room_price": str(room_price),
                "room_url": room_url,
            }

        # Step 1: Extract pushed blocks and merge
        blocks = extract_next_f_blocks(html_doc)
        merged_text = "".join(blocks)

        # Step 2: Extract embedded JSON
        parsed_json = extract_json_from_text(merged_text)
        parsed_room = []
        for room in parsed_json.get("availableRentals")[0]:
            extracted_room = extract_room_info(room)
            if extracted_room:
                parsed_room.append(extracted_room)
        return parsed_room
