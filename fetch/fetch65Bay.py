from fetch.fetch import Fetch


class Fetch65Bay(Fetch):
    def __init__(self, driver, browser):
        super().__init__(driver, browser)
        self.base_url = "https://www.65bay.com"
        self.room_type_map = [
            ("Studio", "Studio"),
            ("^1 bedroom / 1 bathroom$", "1B1B"),
            ("^2 bedrooms / 1 bathroom$", "2B1B"),
            ("^2 bedrooms / 2 bathrooms$", "2B2B"),
            ("^3 bedrooms / 2 bathrooms$", "3B2B"),
        ]

    def fetch_web(self):
        self.get_url_with_retry(self.url)
        availability_buttons = self.wait_until_xpath(
            '//button[contains(@class, "applyButton") and text()="Availability"]'
        )
        room_hrefs = []
        for button in availability_buttons:
            onclick_command = button.get_attribute("onclick")
            property_id = self.get_substring_by_regex(onclick_command, r"myOlePropertyId=(\d+)&")
            floor_plans = self.get_substring_by_regex(onclick_command, r"floorPlans=(\d+)")
            room_hrefs.append(
                f"{self.base_url}/availableunits.aspx?myOlePropertyId={property_id}&floorPlans={floor_plans}"
            )
        self.room_detail_urls = []
        for room_href in room_hrefs:
            self.fetch_room(room_href)
        for room_detail_url in self.room_detail_urls:
            self.fetch_room_detail(room_detail_url)

    def fetch_room(self, room_href):
        self.get_url_with_retry(room_href)
        select_buttons = self.wait_until_xpath(
            '//input[contains(@class, "UnitSelect") and @value="Select"]'
        )
        for button in select_buttons:
            onclick_command = button.get_attribute("onclick")
            room_detail_url = self.get_substring_by_regex(onclick_command, r"SetTermsUrl\('(.*)'\)")
            self.room_detail_urls.append(f"{self.base_url}/{room_detail_url}")

    def fetch_room_detail(self, room_detail_url):
        self.get_url_with_retry(room_detail_url)
        first_row = self.wait_until_xpath('//div[@id="lease_info_panel"]/div[1]')[0]
        room_number = first_row.find_element_by_xpath(".//span[@class='font-semibold']").text
        room_type = self.wait_until_xpath('//span[@data-selenium-id="TermsFPBedBath"]')[0].text
        move_in_date = self.wait_until_xpath("//input[@id='MoveInDate']")[0].get_attribute("value")
        room_price = self.wait_until_xpath("//div[@class='ysp']")[0].text.replace("/month", "")
        self.add_room_info(
            room_number=room_number,
            room_type=room_type,
            move_in_date=move_in_date,
            room_price=room_price,
            room_url=room_detail_url,
        )
