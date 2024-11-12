from fetch.fetch import Fetch


class FetchTFC(Fetch):
    def fetch_web(self):
        self.get_url_with_retry(self.url)
        rooms = self.wait_until_xpath('//a[@role="listitem"]')
        for room in rooms:
            if room.get_attribute("target") == "_blank":
                continue
            room_text = room.text
            if "View" not in room_text or "$" not in room_text:
                continue
            room_url = room.get_attribute("href")
            building_name = room.find_element_by_xpath(".//h2[@class='heading-3 tile-title']").text
            building_location = room.find_element_by_xpath(".//span[@class='heading-4']").text
            room_type = (
                room.find_element_by_xpath(".//span[@class='tile-title']")
                .text.replace(" Bed, ", "B")
                .replace(" Bath", "B")
            )
            room_price = room.find_element_by_xpath(".//span[@class='tile-subtitle']").text
            room_number = room.find_element_by_xpath(".//div[@class='tile-footer']/span[1]").text
            merged_building_room_number = f"[{building_location}] {building_name} {room_number}"

            self.add_room_info(
                room_number=merged_building_room_number,
                room_type=room_type,
                move_in_date="Available Now",
                room_price=room_price,
                room_url=room_url,
            )
