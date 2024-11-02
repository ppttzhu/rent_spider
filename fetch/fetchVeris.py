from time import sleep

from selenium.webdriver.common.by import By

from fetch.fetch import Fetch


class FetchVeris(Fetch):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.room_type_map = [
            ("^Studio / 1 Bath$", "Studio"),
            ("^1 Bed / 1 Bath$", "1B1B"),
            ("^2 Beds / 1 Bath$", "2B1B"),
            ("^2 Bed / 1 Bath$", "2B1B"),
            ("^2 Beds / 2 Bath$", "2B2B"),
            ("^2 Bed / 2 Bath$", "2B2B"),
            ("^2 Beds / 2.5 Bath$", "2B2.5B"),
            ("^2 Bed / 2.5 Bath$", "2B2.5B"),
            ("^3 Beds / 2 Bath$", "3B2B"),
            ("^3 Bed / 2 Bath$", "3B2B"),
        ]

    def fetch_web(self):
        self.get_url_with_retry(self.url)
        view_more_button = self.wait_until_xpath(
            "//div[@class='prop-details-view-more-btn']"
        )[0]
        self.move_to_center(view_more_button)
        view_more_button.click()

        rooms = self.wait_until_xpath('//div[@class="omg-results-card "]')
        for room in rooms:
            sleep(1)
            room_info = room.find_elements(
                by=By.XPATH,
                value='.//div[contains(@class, "omg-results-card-body-element") and contains(@class, "display-floorplan-details")]',
            )
            room_number = room_info[0].text
            move_in_date = room_info[2].text
            room_price = room_info[3].text

            self.move_to_center(room_info[0])
            room_info[0].click()
            sleep(1)
            popup = self.wait_until_xpath(
                '//div[contains(@class, "paoc-cb-popup-body") and contains(@style, "display: block")]'
            )[0]
            bed_count = (
                popup.find_element(by=By.XPATH, value=".//span[@class='takeover-beds']")
                .text.lower()
                .replace("beds", "")
                .replace("bed", "")
                .replace(" ", "")
            )
            bath_count = (
                popup.find_element(
                    by=By.XPATH, value=".//span[@class='takeover-baths']"
                )
                .text.lower()
                .replace("baths", "")
                .replace("bath", "")
                .replace(" ", "")
            )

            self.add_room_info(
                room_number=room_number,
                room_type=f"{bed_count}B{bath_count}B",
                move_in_date=move_in_date,
                room_price=room_price,
            )

            close_button = popup.find_element(
                by=By.XPATH, value='.//a[contains(@class, "paoc-pro-close-popup")]'
            )
            close_button.click()
