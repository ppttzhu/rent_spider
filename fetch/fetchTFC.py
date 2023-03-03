from fetch.fetch import Fetch


class FetchTFC(Fetch):
    def fetch_web(self):
        self.get_url_with_retry(self.url)

        select_button = self.wait_until_xpath('//button[@id="dropdown-neighborhoods-dropdown"]')
        select_button[0].click()

        select_dropdown = self.wait_until_xpath('//div[@id="portal-neighborhoods-dropdown"]')
        select_all = select_dropdown[0].find_element_by_xpath(
            ".//label[contains(@id, 'label-select-all')]"
        )
        select_all.click()

        rooms = self.wait_until_xpath('//a[@role="listitem"]')

        for room in rooms:
            room_url = room.get_attribute("href")
            building_name = room.find_element_by_xpath(".//span[@class='heading-4']").text
            room_type = (
                room.find_element_by_xpath(".//span[@class='tile-title']")
                .text.replace(" Bed, ", "B")
                .replace(" Bath", "B")
            )
            room_price = room.find_element_by_xpath(".//span[@class='tile-subtitle']").text
            room_number = room.find_element_by_xpath(".//div[@class='tile-footer']/span[1]").text
            merged_building_room_number = f"{building_name} {room_number}"

            self.add_room_info(
                room_number=merged_building_room_number,
                room_type=room_type,
                move_in_date="Available Now",
                room_price=room_price,
                room_url=room_url,
            )
