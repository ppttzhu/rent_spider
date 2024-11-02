from time import sleep

from selenium.webdriver.common.by import By

from fetch.fetch import Fetch


class FetchVeris(Fetch):
    def fetch_web(self):
        self.get_url_with_retry(self.url)
        view_more_button = self.wait_until_xpath(
            "//div[@class='prop-details-view-more-btn']"
        )[0]
        self.close_popup()
        sleep(1)
        self.move_to_center(view_more_button)
        sleep(1)
        view_more_button.click()
        sleep(1)
        rooms = self.wait_until_xpath('//div[@class="omg-results-card "]')
        for room in rooms:
            sleep(0.5)
            room_info = room.find_elements(
                by=By.XPATH,
                value='.//div[contains(@class, "omg-results-card-body-element") and contains(@class, "display-floorplan-details")]',
            )

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
            room_prefix = popup.find_element(by=By.XPATH, value=".//div[contains(@class, 'floorplan-name')]").text
            units = popup.find_elements(by=By.XPATH, value=".//div[@class='basis-1/2']")
            for unit in units:
                info = unit.find_elements(
                    by=By.XPATH, value=".//div[contains(@class, 'text-sm')]"
                )
                room_number = f'{room_prefix} {info[0].text}'
                room_price = info[1].text.replace("From", "").replace(" ", "")
                move_in_date = info[2].text
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

    def close_popup(self):
        popup = self.driver.find_elements(
            by=By.XPATH,
            value='//div[contains(@class, "paoc-cb-popup-body") and contains(@style, "display: block")]',
        )
        if not popup:
            return
        close_button = popup[0].find_element(
            by=By.XPATH, value='.//a[contains(@class, "paoc-pro-close-popup")]'
        )
        close_button.click()
