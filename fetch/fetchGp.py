import re

from bs4 import BeautifulSoup

from fetch.fetch981Management import Fetch981Management


class FetchGp(Fetch981Management):

    def fetch_room_info(self, room_url):
        html_doc = self.get_html_doc(room_url)
        self.check_blocked(html_doc)
        soup = BeautifulSoup(html_doc, "html.parser")
        room_type = self.parse_room_type(soup)
        cards = soup.find_all(lambda tag: tag.name == 'div' and tag.get('class') == ['card'])
        for card in cards: 
            apartment = card.find('h3', {"class": "card-title"})
            room_number = apartment.text.replace('\n','').replace(' ','').replace('Apartment:#','')

            rent = card.find('p', {"class": "card-subtitle"})
            room_price = rent.text.replace('Starting at:','').replace(' ','').replace('\n','')

            button = self.find_all_contains(card,'button', 'Select_')[0]
            onclick = button.attrs['onclick']
            match = re.search("href='.*'", onclick)
            html = match.group(0).replace('href=', '').replace("'", '')

            move_in_date = self.parse_move_in_date(html)

            self.add_room_info(
                room_number=room_number,
                room_type=room_type,
                move_in_date=move_in_date,
                room_price=room_price,
                room_url=html
            )
