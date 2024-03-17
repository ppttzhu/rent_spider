import re
from datetime import date, timedelta

from bs4 import BeautifulSoup
from dateutil import parser

from fetch.fetch import Fetch


class Fetch981Management(Fetch):
    def fetch_web(self):
        html_doc = self.get_html_doc(self.url)
        self.check_blocked(html_doc)
        soup = BeautifulSoup(html_doc, "html.parser")
        if self.soup_check_contain(soup, "p", "not available"):
            return
     
        apply_buttons = soup.find_all('a', {"href": re.compile(f'.*/floorplans.*'), "name": "applynow"})
        base_url = '/'.join(self.url.split('/')[:3])
        room_urls = [base_url + button.attrs['href'] for button in apply_buttons]
        for url in list(set(room_urls)):
            self.fetch_room_info(url)

    def fetch_room_info(self, room_url):
        html_doc = self.get_html_doc(room_url)
        self.check_blocked(html_doc)
        soup = BeautifulSoup(html_doc, "html.parser")
        room_type = self.parse_room_type(soup)
        rows = self.find_all_contains(soup,'tr', 'urow')
        for row in rows: 
            apartment = self.find_all_contains(row,'td', 'Apt')[0]
            room_number = apartment.text.replace('\n','').replace(' ','').replace('Apartment:#','')

            rent = self.find_all_contains(row,'td', 'Rent')[0]
            room_price = rent.text.split(' ')[0].replace('Rent:','')

            button = self.find_all_contains(row,'button', 'Select_')[0]
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

    def find_all_contains(self, soup, tag, text):
        return soup.find_all(tag, {"data-selenium-id": re.compile(f'.*{text}.*')})
    
    def parse_move_in_date(self, html):
        move_in_date = ''
        move_in_date_index = html.find('MoveInDate')
        if move_in_date_index:
            for i in range(move_in_date_index + len('MoveInDate') + 1, len(html)):
                if html[i] == "&":
                    break
                move_in_date += html[i]
        tomorrow = date.today() + timedelta(days=1)
        move_in_datetime = parser.parse(move_in_date).date()
        if move_in_datetime <= tomorrow:
            return 'Available Now'
        return move_in_date

    def parse_room_type(self, soup):
        room_header = soup.find('div', {"id": 'available-units-container'}).text.lower()
        if 'studio' in room_header:
            return 'Studio'
        bedroom, bathroom = 0, 0
        for i in range(1, 5):
            if f'{i} bedroom' in room_header:
                bedroom = i
        for i in range(1, 5):
            if f'{i} bathroom' in room_header:
                bathroom = i
        return f'{bedroom}B{bathroom}B'
        


