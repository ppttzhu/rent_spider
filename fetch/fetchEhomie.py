import re
from datetime import datetime, timedelta
from time import sleep

import constants as c

from fetch.fetch import Fetch


class FetchEhomie(Fetch):
    def __init__(self, driver, browser):
        super().__init__(driver, browser)
        self.sleep_second = 0.5

    def fetch_web(self):
        page = 1
        while page < 100:
            sleep(self.sleep_second)
            self.get_url_with_retry(f"{self.url}-page{page}")
            rooms = self.wait_until_xpath('//div[@class="house-list"]/a')
            target_rooms_info = []
            for room in rooms:
                title = self.wait_until_xpath('.//div[@class="item-info-title"]', room)[0].text
                if "求" in title:
                    continue
                date_string = self.wait_until_xpath('.//div[@class="item-info-date"]', room)[0].text
                date = datetime.strptime(date_string.replace("发布时间：", ""), "%Y-%m-%d %H:%M")
                target_rooms_info.append(
                    {
                        c.ROOM_URL_COLUMN: room.get_attribute("href"),
                        c.ROOM_TITLE_COLUMN: title,
                        c.POST_DATE_COLUMN: date,
                    }
                )
            for room_info in target_rooms_info:
                if room_info[c.POST_DATE_COLUMN] < datetime.now() - timedelta(days=30):
                    return
                self.fetch_room_info(room_info)
            page += 1

    def fetch_room_info(self, room_info):
        sleep(self.sleep_second)
        self.get_url_with_retry(room_info[c.ROOM_URL_COLUMN])
        detail_info = self.wait_until_xpath('//pre[@class="detail-desc-info"]')[0].text
        if "求" in detail_info:
            return
        price = self.wait_until_xpath('//div[@class="detail-info-price"]')[0].text
        move_in_date = self.wait_until_xpath('//div[@class="detail-info-date"]')[0].text.replace(
            "租期时间：", ""
        )
        room_type = self.find_room_type(room_info[c.ROOM_TITLE_COLUMN] + detail_info)
        self.add_sublease_info(
            {
                **room_info,
                c.ROOM_TYPE_COLUMN: room_type,
                c.MOVE_IN_DATE_COLUMN: move_in_date,
                c.ROOM_PRICE_COLUMN: price,
                c.POST_DATE_COLUMN: room_info[c.POST_DATE_COLUMN].strftime("%Y-%m-%d %H:%M:%S"),
            }
        )

    def find_room_type(self, info):
        info = info.upper()
        if "STUDIO" in info:
            return "0Studio"
        room_type_regex = re.compile(r"\dB\dB")
        search_result = room_type_regex.search(info)
        if not search_result:
            return "?"
        return search_result.group()
