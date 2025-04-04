import argparse
import configparser
import os
from enum import Enum


class Platform(Enum):
    DEV = 1
    PAW_HOURLY = 2 
    PAW_HALF_HOURLY = 3 
    PAW_TWICE_DAILY = 4 


class RentType(Enum):
    RENTAL = 1
    SUBLEASE = 2


FREQUENCY_MAP = {
    Platform.PAW_HOURLY: "三小时一次",
    Platform.PAW_HALF_HOURLY: "半小时一次",
    Platform.PAW_TWICE_DAILY: "每日两次",
}

PLATFORM = None
IS_REMOTE = False
NEED_UPDATE_WEBSITE = None
WEBSITES_TARGETS = None
RENT_TYPE = None

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
SNAPSHOT_DIR = os.path.join(ROOT_DIR, "../snapshot.xlsx")
CONFIG = configparser.ConfigParser()
CONFIG.read(os.path.join(ROOT_DIR, "secrets.cfg"))

MINUTES_BETWEEN_FETCH = 10
TOTAL_DURATION_IN_MINUTES = 60
WEB_DRIVER_TIMEOUT_SECOND = 30
SE_SLEEP_MIN_SECOND = 20
SE_SLEEP_MAX_SECOND = 25
PROXY_GET_URL_MAX_RETRY = 5


WEBSITE_TABLE_NAME = "website"
WEBSITE_NAME_COLUMN = "website_name"
WEBSITE_LOCATION_COLUMN = "location"
WEBSITE_URL_COLUMN = "url"
WEBSITE_PRIORITY_COLUMN = "priority"
WEBSITE_RENT_TYPE = "rent_type"

ROOM_TABLE_NAME = "room"
SUBLEASE_TABLE_NAME = "sublease"
ROOM_HISTORY_TABLE_NAME = "room_history"
FETCH_STATUS_TABLE_NAME = "fetch_status"
ROOM_NUMBER_COLUMN = "room_number"
ROOM_URL_COLUMN = "room_url"
ROOM_TYPE_COLUMN = "room_type"
MOVE_IN_DATE_COLUMN = "move_in_date"
ROOM_PRICE_COLUMN = "room_price"
FETCH_DATE_COLUMN = "fetch_date"
LATEST_FETCH_DATE_COLUMN = "latest_fetch_date"
LATEST_FETCH_WARNING = "latest_fetch_warning"
ROOM_COUNT_COLUMN = "room_count"
ROOM_TITLE_COLUMN = "room_title"
POST_DATE_COLUMN = "post_date"
ROOM_TABLE_PRIMARY_KEY = [WEBSITE_NAME_COLUMN, ROOM_NUMBER_COLUMN]
SUBLEASE_TABLE_PRIMARY_KEY = [WEBSITE_NAME_COLUMN, ROOM_NUMBER_COLUMN]
ROOM_TABLE_COLUMNS = [
    WEBSITE_NAME_COLUMN,
    ROOM_TYPE_COLUMN,
    ROOM_NUMBER_COLUMN,
    MOVE_IN_DATE_COLUMN,
    ROOM_PRICE_COLUMN,
]
SUBLEASE_TABLE_COLUMNS = [
    WEBSITE_NAME_COLUMN,
    ROOM_URL_COLUMN,
    ROOM_TITLE_COLUMN,
    ROOM_TYPE_COLUMN,
    MOVE_IN_DATE_COLUMN,
    ROOM_PRICE_COLUMN,
    POST_DATE_COLUMN,
]
FETCH_STATUS_COLUMNS = [
    WEBSITE_NAME_COLUMN,
    ROOM_COUNT_COLUMN,
    FETCH_DATE_COLUMN,
]
ROOM_TABLE_COLUMNS_NAME = ["房源网站", "户型", "房号", "入住时间", "房价"]
SUBLEASE_TABLE_COLUMNS_NAME = [
    "房源网站",
    "转租信息",
    "户型",
    "入住时间",
    "房价",
    "发布时间",
]
FETCH_DATE_COLUMN_NAME = "抓取时间"
FETCH_FREQUENCY_COLUMN_NAME = "抓取频率"
LATEST_FETCH_DATE_COLUMN_NAME = "更新时间"
ROOM_COUNT_COLUMN_NAME = "房间数量"
FETCH_STATUS_COLUMNS_NAME = ["房源网站", ROOM_COUNT_COLUMN_NAME, FETCH_DATE_COLUMN_NAME]

WEBSITE_ROOM_VIEW_NAME = "v_website_room"
WEBSITE_SUBLEASE_VIEW_NAME = "v_website_sublease"
WEBSITE_ROOM_HISTORY_VIEW_NAME = "v_website_room_history"
FETCH_STATUS_VIEW_NAME = "v_fetch_status"
WEBSITE_ROOM_VIEW_ADDITIONAL_COLUMNS = [
    ROOM_URL_COLUMN,
    WEBSITE_URL_COLUMN,
    WEBSITE_LOCATION_COLUMN,
    WEBSITE_PRIORITY_COLUMN,
]
WEBSITE_ROOM_VIEW_COLUMNS = ROOM_TABLE_COLUMNS + WEBSITE_ROOM_VIEW_ADDITIONAL_COLUMNS
WEBSITE_SUBLEASE_VIEW_COLUMNS = (
    SUBLEASE_TABLE_COLUMNS + WEBSITE_ROOM_VIEW_ADDITIONAL_COLUMNS
)

WEBSITES = [
    {
        WEBSITE_URL_COLUMN: "https://streeteasy.com/building/the-biltmore",
        WEBSITE_NAME_COLUMN: "Biltmore",
        "parent_class_name": "StreetEasy",
        "class_name": "Biltmore",
        "platform": Platform.PAW_TWICE_DAILY,
        "location": "Manhattan",
        WEBSITE_RENT_TYPE: RentType.RENTAL,
    },
    {
        WEBSITE_URL_COLUMN: "https://streeteasy.com/building/lyra-555-west-38-street-new_york",
        WEBSITE_NAME_COLUMN: "Lyra",
        "parent_class_name": "StreetEasy",
        "class_name": "Lyra",
        "platform": Platform.PAW_TWICE_DAILY,
        "location": "Manhattan",
        WEBSITE_RENT_TYPE: RentType.RENTAL,
    },
    {
        WEBSITE_URL_COLUMN: "https://streeteasy.com/building/mima-450-west-42-street-new_york",
        WEBSITE_NAME_COLUMN: "Mima",
        "parent_class_name": "StreetEasy",
        "class_name": "Mima",
        "platform": Platform.PAW_TWICE_DAILY,
        "location": "Manhattan",
        WEBSITE_RENT_TYPE: RentType.RENTAL,
    },
    {
        WEBSITE_URL_COLUMN: "https://streeteasy.com/building/555ten-555-10th-avenue-manhattan",
        WEBSITE_NAME_COLUMN: "555 Ten",
        "parent_class_name": "StreetEasy",
        "class_name": "555Ten",
        "platform": Platform.PAW_TWICE_DAILY,
        "location": "Manhattan",
        WEBSITE_RENT_TYPE: RentType.RENTAL,
    },
    {
        WEBSITE_URL_COLUMN: "https://streeteasy.com/building/the-ritz-plaza",
        WEBSITE_NAME_COLUMN: "Ritz Plaza",
        "parent_class_name": "StreetEasy",
        "class_name": "RitzPlaza",
        "platform": Platform.PAW_TWICE_DAILY,
        "location": "Manhattan",
        WEBSITE_RENT_TYPE: RentType.RENTAL,
    },
    {
        WEBSITE_URL_COLUMN: "https://streeteasy.com/building/the-epic",
        WEBSITE_NAME_COLUMN: "The Epic",
        "parent_class_name": "StreetEasy",
        "class_name": "TheEpic",
        "platform": Platform.PAW_TWICE_DAILY,
        "location": "Manhattan",
        WEBSITE_RENT_TYPE: RentType.RENTAL,
    },
    {
        WEBSITE_URL_COLUMN: "https://streeteasy.com/building/the-continental",
        WEBSITE_NAME_COLUMN: "The Continental",
        "class_name": "TheContinental",
        "parent_class_name": "StreetEasy",
        "platform": Platform.PAW_TWICE_DAILY,
        "location": "Manhattan",
        WEBSITE_RENT_TYPE: RentType.RENTAL,
    },
    {
        WEBSITE_URL_COLUMN: "https://streeteasy.com/building/the-dylan",
        WEBSITE_NAME_COLUMN: "The Dylan",
        "parent_class_name": "StreetEasy",
        "class_name": "TheDylan",
        "platform": Platform.PAW_TWICE_DAILY,
        "location": "Manhattan",
        WEBSITE_RENT_TYPE: RentType.RENTAL,
    },
    {
        WEBSITE_URL_COLUMN: "https://streeteasy.com/building/the-max",
        WEBSITE_NAME_COLUMN: "The Max",
        "parent_class_name": "StreetEasy",
        "class_name": "TheMax",
        "platform": Platform.PAW_TWICE_DAILY,
        "location": "Manhattan",
        WEBSITE_RENT_TYPE: RentType.RENTAL,
    },
    {
        WEBSITE_URL_COLUMN: "https://streeteasy.com/building/gotham-west",
        WEBSITE_NAME_COLUMN: "Gotham West",
        "parent_class_name": "StreetEasy",
        "class_name": "GothamWest",
        "platform": Platform.PAW_TWICE_DAILY,
        "location": "Manhattan",
        WEBSITE_RENT_TYPE: RentType.RENTAL,
    },
    {
        WEBSITE_URL_COLUMN: "https://streeteasy.com/building/sky-605-west-42-street-new_york",
        WEBSITE_NAME_COLUMN: "Sky",
        "parent_class_name": "StreetEasy",
        "class_name": "Sky",
        "platform": Platform.PAW_TWICE_DAILY,
        "location": "Manhattan",
        WEBSITE_RENT_TYPE: RentType.RENTAL,
    },
    {
        WEBSITE_URL_COLUMN: "https://streeteasy.com/building/the-victory",
        WEBSITE_NAME_COLUMN: "The Victory",
        "parent_class_name": "StreetEasy",
        "class_name": "TheVictory",
        "platform": Platform.PAW_TWICE_DAILY,
        "location": "Manhattan",
        WEBSITE_RENT_TYPE: RentType.RENTAL,
    },
    {
        WEBSITE_URL_COLUMN: "https://streeteasy.com/building/eos-100-west-31st-street-new_york",
        WEBSITE_NAME_COLUMN: "EOS",
        "parent_class_name": "StreetEasy",
        "class_name": "EOS",
        "platform": Platform.PAW_TWICE_DAILY,
        "location": "Manhattan",
        WEBSITE_RENT_TYPE: RentType.RENTAL,
    },
    {
        WEBSITE_URL_COLUMN: "https://streeteasy.com/building/silver-towers",
        WEBSITE_NAME_COLUMN: "Silver Towers",
        "parent_class_name": "StreetEasy",
        "class_name": "SilverTowers",
        "platform": Platform.PAW_TWICE_DAILY,
        "location": "Manhattan",
        WEBSITE_RENT_TYPE: RentType.RENTAL,
    },
    {
        WEBSITE_URL_COLUMN: "https://streeteasy.com/building/one-manhattan-square",
        WEBSITE_NAME_COLUMN: "OMS",
        "parent_class_name": "StreetEasy",
        "class_name": "OMS",
        "platform": Platform.PAW_TWICE_DAILY,
        "location": "Manhattan",
        WEBSITE_RENT_TYPE: RentType.RENTAL,
    },
    {
        WEBSITE_URL_COLUMN: "https://streeteasy.com/building/101-west-end-avenue-new_york",
        WEBSITE_NAME_COLUMN: "101 West End",
        "parent_class_name": "StreetEasy",
        "class_name": "101WestEnd",
        "platform": Platform.PAW_TWICE_DAILY,
        "location": "Manhattan",
        WEBSITE_RENT_TYPE: RentType.RENTAL,
    },
    {
        WEBSITE_URL_COLUMN: "https://streeteasy.com/building/21-west-end-avenue-new_york",
        WEBSITE_NAME_COLUMN: "21 West End Ave",
        "parent_class_name": "StreetEasy",
        "class_name": "21WestEndAve",
        "platform": Platform.PAW_TWICE_DAILY,
        "location": "Manhattan",
        WEBSITE_RENT_TYPE: RentType.RENTAL,
    },
    {
        WEBSITE_URL_COLUMN: "https://streeteasy.com/building/via-57-west",
        WEBSITE_NAME_COLUMN: "Via 57 West",
        "parent_class_name": "StreetEasy",
        "class_name": "Via57West",
        "platform": Platform.PAW_TWICE_DAILY,
        "location": "Manhattan",
        WEBSITE_RENT_TYPE: RentType.RENTAL,
    },
    {
        WEBSITE_URL_COLUMN: "https://streeteasy.com/building/helena-57-west",
        WEBSITE_NAME_COLUMN: "Helena 57 West",
        "parent_class_name": "StreetEasy",
        "class_name": "Helena57West",
        "platform": Platform.PAW_TWICE_DAILY,
        "location": "Manhattan",
        WEBSITE_RENT_TYPE: RentType.RENTAL,
    },
    {
        WEBSITE_URL_COLUMN: "https://streeteasy.com/building/mercedes-house",
        WEBSITE_NAME_COLUMN: "Mercedes House",
        "parent_class_name": "StreetEasy",
        "class_name": "MercedesHouse",
        "platform": Platform.PAW_TWICE_DAILY,
        "location": "Manhattan",
        WEBSITE_RENT_TYPE: RentType.RENTAL,
    },
    {
        WEBSITE_URL_COLUMN: "https://streeteasy.com/building/535w43-535-west-43-street-new_york",
        WEBSITE_NAME_COLUMN: "535 W 43rd St",
        "parent_class_name": "StreetEasy",
        "class_name": "535W43rdSt",
        "platform": Platform.PAW_TWICE_DAILY,
        "location": "Manhattan",
        WEBSITE_RENT_TYPE: RentType.RENTAL,
    },
    {
        WEBSITE_URL_COLUMN: "https://streeteasy.com/building/the-landon",
        WEBSITE_NAME_COLUMN: "The Landon",
        "parent_class_name": "StreetEasy",
        "class_name": "TheLandon",
        "platform": Platform.PAW_TWICE_DAILY,
        "location": "Manhattan",
        WEBSITE_RENT_TYPE: RentType.RENTAL,
    },
    {
        WEBSITE_URL_COLUMN: "https://streeteasy.com/building/riverbank-560-west-43-street-new_york",
        WEBSITE_NAME_COLUMN: "Riverbank",
        "parent_class_name": "StreetEasy",
        "class_name": "Riverbank",
        "platform": Platform.PAW_TWICE_DAILY,
        "location": "Manhattan",
        WEBSITE_RENT_TYPE: RentType.RENTAL,
    },
    {
        WEBSITE_URL_COLUMN: "https://streeteasy.com/building/river-place",
        WEBSITE_NAME_COLUMN: "River Place",
        "parent_class_name": "StreetEasy",
        "class_name": "RiverPlace",
        "platform": Platform.PAW_TWICE_DAILY,
        "location": "Manhattan",
        WEBSITE_RENT_TYPE: RentType.RENTAL,
    },
    {
        WEBSITE_URL_COLUMN: "https://streeteasy.com/building/hudson-36",
        WEBSITE_NAME_COLUMN: "Hudson 36",
        "parent_class_name": "StreetEasy",
        "class_name": "Hudson36",
        "platform": Platform.PAW_TWICE_DAILY,
        "location": "Manhattan",
        WEBSITE_RENT_TYPE: RentType.RENTAL,
    },
    {
        WEBSITE_URL_COLUMN: "https://streeteasy.com/building/606w30-606-west-30-street-new_york",
        WEBSITE_NAME_COLUMN: "606 W 30",
        "parent_class_name": "StreetEasy",
        "class_name": "606W30",
        "platform": Platform.PAW_TWICE_DAILY,
        "location": "Manhattan",
        WEBSITE_RENT_TYPE: RentType.RENTAL,
    },
    {
        WEBSITE_URL_COLUMN: "https://streeteasy.com/building/3-eleven",
        WEBSITE_NAME_COLUMN: "3 Eleven",
        "parent_class_name": "StreetEasy",
        "class_name": "3Eleven",
        "platform": Platform.PAW_TWICE_DAILY,
        "location": "Manhattan",
        WEBSITE_RENT_TYPE: RentType.RENTAL,
    },
    {
        WEBSITE_URL_COLUMN: "https://streeteasy.com/building/henry-hall",
        WEBSITE_NAME_COLUMN: "Henry Hall",
        "parent_class_name": "StreetEasy",
        "class_name": "HenryHall",
        "platform": Platform.PAW_TWICE_DAILY,
        "location": "Manhattan",
        WEBSITE_RENT_TYPE: RentType.RENTAL,
    },
    {
        WEBSITE_URL_COLUMN: "https://streeteasy.com/building/445-west-35-street-new_york",
        WEBSITE_NAME_COLUMN: "445W 35th",
        "parent_class_name": "StreetEasy",
        "class_name": "445W35th",
        "platform": Platform.PAW_TWICE_DAILY,
        "location": "Manhattan",
        WEBSITE_RENT_TYPE: RentType.RENTAL,
    },
    {
        WEBSITE_URL_COLUMN: "https://streeteasy.com/building/the-lewis",
        WEBSITE_NAME_COLUMN: "The Lewis",
        "parent_class_name": "StreetEasy",
        "class_name": "TheLewis",
        "platform": Platform.PAW_TWICE_DAILY,
        "location": "Manhattan",
        WEBSITE_RENT_TYPE: RentType.RENTAL,
    },
    {
        WEBSITE_URL_COLUMN: "https://streeteasy.com/building/the-eugene",
        WEBSITE_NAME_COLUMN: "The Eugene",
        "parent_class_name": "StreetEasy",
        "class_name": "TheEugene",
        "platform": Platform.PAW_TWICE_DAILY,
        "location": "Manhattan",
        WEBSITE_RENT_TYPE: RentType.RENTAL,
    },
    {
        WEBSITE_URL_COLUMN: "https://www.tower28lic.com/floorplans",
        WEBSITE_NAME_COLUMN: "Tower 28",
        "class_name": "Tower28",
        "parent_class_name": "Heatherwood",
        "platform": Platform.PAW_HOURLY,
        "location": "LIC",
        WEBSITE_RENT_TYPE: RentType.RENTAL,
    },
    {
        WEBSITE_URL_COLUMN: "https://www.27on27th.com/floorplans",
        WEBSITE_NAME_COLUMN: "27 on 27th",
        "class_name": "27on27th",
        "parent_class_name": "Heatherwood",
        "platform": Platform.PAW_HOURLY,
        "location": "LIC",
        WEBSITE_RENT_TYPE: RentType.RENTAL,
    },
    {
        WEBSITE_URL_COLUMN: "https://jacksonparklic.com/availability/",
        WEBSITE_NAME_COLUMN: "Jackson Park LIC",
        "class_name": "JacksonPark",
        "platform": Platform.PAW_HOURLY,
        "location": "LIC",
        WEBSITE_RENT_TYPE: RentType.RENTAL,
    },
    {
        WEBSITE_URL_COLUMN: "https://streeteasy.com/complex/jackson-park-lic",
        WEBSITE_NAME_COLUMN: "Jackson Park LIC SE",
        "class_name": "JacksonParkAWS",
        "platform": Platform.PAW_TWICE_DAILY,
        "location": "LIC",
        WEBSITE_RENT_TYPE: RentType.RENTAL,
    },
    {
        WEBSITE_URL_COLUMN: "https://streeteasy.com/building/1-qps",
        WEBSITE_NAME_COLUMN: "1 QPS",
        "parent_class_name": "StreetEasy",
        "class_name": "1QPS",
        "platform": Platform.PAW_TWICE_DAILY,
        "location": "LIC",
        WEBSITE_RENT_TYPE: RentType.RENTAL,
    },
    {
        WEBSITE_URL_COLUMN: "https://streeteasy.com/building/5pointz-lic",
        WEBSITE_NAME_COLUMN: "5Pointz",
        "parent_class_name": "StreetEasy",
        "class_name": "5Pointz",
        "platform": Platform.PAW_TWICE_DAILY,
        "location": "LIC",
        WEBSITE_RENT_TYPE: RentType.RENTAL,
    },
    {
        WEBSITE_URL_COLUMN: "https://streeteasy.com/building/rise-lic",
        WEBSITE_NAME_COLUMN: "Rise LIC",
        "parent_class_name": "StreetEasy",
        "class_name": "RiseLIC",
        "platform": Platform.PAW_TWICE_DAILY,
        "location": "LIC",
        WEBSITE_RENT_TYPE: RentType.RENTAL,
    },
    {
        WEBSITE_URL_COLUMN: "https://streeteasy.com/building/sven-29_59-northern-boulevard-long_island_city",
        WEBSITE_NAME_COLUMN: "Sven",
        "parent_class_name": "StreetEasy",
        "class_name": "Sven",
        "platform": Platform.PAW_TWICE_DAILY,
        "location": "LIC",
        WEBSITE_RENT_TYPE: RentType.RENTAL,
    },
    {
        WEBSITE_URL_COLUMN: "https://streeteasy.com/building/dutch-lic",
        WEBSITE_NAME_COLUMN: "Dutch LIC",
        "parent_class_name": "StreetEasy",
        "class_name": "DutchLIC",
        "platform": Platform.PAW_TWICE_DAILY,
        "location": "LIC",
        WEBSITE_RENT_TYPE: RentType.RENTAL,
    },
    {
        WEBSITE_URL_COLUMN: "https://streeteasy.com/building/the-maximilian",
        WEBSITE_NAME_COLUMN: "The Maximilian",
        "parent_class_name": "StreetEasy",
        "class_name": "TheMaximilian",
        "platform": Platform.PAW_TWICE_DAILY,
        "location": "LIC",
        WEBSITE_RENT_TYPE: RentType.RENTAL,
    },
    {
        WEBSITE_URL_COLUMN: "https://streeteasy.com/building/steel-haus",
        WEBSITE_NAME_COLUMN: "Steel Haus",
        "class_name": "SteelHaus",
        "platform": Platform.PAW_TWICE_DAILY,
        "location": "LIC",
        WEBSITE_RENT_TYPE: RentType.RENTAL,
    },
    {
        WEBSITE_URL_COLUMN: "https://streeteasy.com/building/arc-30_02-39-avenue-queens",
        WEBSITE_NAME_COLUMN: "Arc",
        "parent_class_name": "StreetEasy",
        "class_name": "Arc",
        "platform": Platform.PAW_TWICE_DAILY,
        "location": "LIC",
        WEBSITE_RENT_TYPE: RentType.RENTAL,
    },
    {
        WEBSITE_URL_COLUMN: "https://streeteasy.com/building/the-forge",
        WEBSITE_NAME_COLUMN: "Forge",
        "parent_class_name": "StreetEasy",
        "class_name": "Forge",
        "platform": Platform.PAW_TWICE_DAILY,
        "location": "LIC",
        WEBSITE_RENT_TYPE: RentType.RENTAL,
    },
    {
        WEBSITE_URL_COLUMN: "https://streeteasy.com/building/altalic-29_22-northern-boulevard-long_island_city",
        WEBSITE_NAME_COLUMN: "AltaLIC",
        "parent_class_name": "StreetEasy",
        "class_name": "Alta",
        "platform": Platform.PAW_TWICE_DAILY,
        "location": "LIC",
        WEBSITE_RENT_TYPE: RentType.RENTAL,
    },
    {
        WEBSITE_URL_COLUMN: "https://streeteasy.com/building/watermark-lic",
        WEBSITE_NAME_COLUMN: "Watermark",
        "parent_class_name": "StreetEasy",
        "class_name": "Watermark",
        "platform": Platform.PAW_TWICE_DAILY,
        "location": "LIC",
        WEBSITE_RENT_TYPE: RentType.RENTAL,
    },
    {
        WEBSITE_URL_COLUMN: "https://streeteasy.com/building/qlic-41_42-24-street-long_island_city",
        WEBSITE_NAME_COLUMN: "QLIC",
        "parent_class_name": "StreetEasy",
        "class_name": "QLIC",
        "platform": Platform.PAW_TWICE_DAILY,
        "location": "LIC",
        WEBSITE_RENT_TYPE: RentType.RENTAL,
    },
    {
        WEBSITE_URL_COLUMN: "https://streeteasy.com/building/luna-lic",
        WEBSITE_NAME_COLUMN: "Luna",
        "parent_class_name": "StreetEasy",
        "class_name": "Luna",
        "platform": Platform.PAW_TWICE_DAILY,
        "location": "LIC",
        WEBSITE_RENT_TYPE: RentType.RENTAL,
    },
    {
        WEBSITE_URL_COLUMN: "https://streeteasy.com/building/8-court-square-long_island_city",
        WEBSITE_NAME_COLUMN: "8 CourtSquare",
        "parent_class_name": "StreetEasy",
        "class_name": "8CourtSquare",
        "platform": Platform.PAW_TWICE_DAILY,
        "location": "LIC",
        WEBSITE_RENT_TYPE: RentType.RENTAL,
    },
    {
        WEBSITE_URL_COLUMN: "https://streeteasy.com/building/bevel-lic",
        WEBSITE_NAME_COLUMN: "Bevel LIC",
        "parent_class_name": "StreetEasy",
        "class_name": "BevelLIC",
        "platform": Platform.PAW_TWICE_DAILY,
        "location": "LIC",
        WEBSITE_RENT_TYPE: RentType.RENTAL,
    },
    {
        WEBSITE_URL_COLUMN: "https://streeteasy.com/building/one-lic",
        WEBSITE_NAME_COLUMN: "One LIC",
        "parent_class_name": "StreetEasy",
        "class_name": "OneLIC",
        "platform": Platform.PAW_TWICE_DAILY,
        "location": "LIC",
        WEBSITE_RENT_TYPE: RentType.RENTAL,
    },
    {
        WEBSITE_URL_COLUMN: "https://streeteasy.com/building/star-tower-lic",
        WEBSITE_NAME_COLUMN: "Star Tower",
        "parent_class_name": "StreetEasy",
        "class_name": "StarTower",
        "platform": Platform.PAW_TWICE_DAILY,
        "location": "LIC",
        WEBSITE_RENT_TYPE: RentType.RENTAL,
    },
    {
        WEBSITE_URL_COLUMN: "https://streeteasy.com/building/hero-condominium",
        WEBSITE_NAME_COLUMN: "Hero",
        "parent_class_name": "StreetEasy",
        "class_name": "Hero",
        "platform": Platform.PAW_TWICE_DAILY,
        "location": "LIC",
        WEBSITE_RENT_TYPE: RentType.RENTAL,
    },
    {
        WEBSITE_URL_COLUMN: "https://streeteasy.com/building/galerie-condominium",
        WEBSITE_NAME_COLUMN: "Galerie",
        "parent_class_name": "StreetEasy",
        "class_name": "Galerie",
        "platform": Platform.PAW_TWICE_DAILY,
        "location": "LIC",
        WEBSITE_RENT_TYPE: RentType.RENTAL,
    },
    {
        WEBSITE_URL_COLUMN: "https://streeteasy.com/building/22_22-jackson-avenue-long_island_city",
        WEBSITE_NAME_COLUMN: "22-22 Jackson Ave",
        "parent_class_name": "StreetEasy",
        "class_name": "JacksonAve",
        "platform": Platform.PAW_TWICE_DAILY,
        "location": "LIC",
        WEBSITE_RENT_TYPE: RentType.RENTAL,
    },
    {
        WEBSITE_URL_COLUMN: "https://streeteasy.com/building/aurora-condominium",
        WEBSITE_NAME_COLUMN: "Aurora",
        "parent_class_name": "StreetEasy",
        "class_name": "Aurora",
        "platform": Platform.PAW_TWICE_DAILY,
        "location": "LIC",
        WEBSITE_RENT_TYPE: RentType.RENTAL,
    },
    {
        WEBSITE_URL_COLUMN: "https://streeteasy.com/building/dutch-house",
        WEBSITE_NAME_COLUMN: "Dutch House",
        "parent_class_name": "StreetEasy",
        "class_name": "DutchHouse",
        "platform": Platform.PAW_TWICE_DAILY,
        "location": "LIC",
        WEBSITE_RENT_TYPE: RentType.RENTAL,
    },
    {
        WEBSITE_URL_COLUMN: "https://streeteasy.com/building/packard-square",
        WEBSITE_NAME_COLUMN: "Packard Square",
        "parent_class_name": "StreetEasy",
        "class_name": "PackardSquare",
        "platform": Platform.PAW_TWICE_DAILY,
        "location": "LIC",
        WEBSITE_RENT_TYPE: RentType.RENTAL,
    },
    {
        WEBSITE_URL_COLUMN: "https://streeteasy.com/building/packard-square-west",
        WEBSITE_NAME_COLUMN: "Packard Square West",
        "parent_class_name": "StreetEasy",
        "class_name": "PackardSquareWest",
        "platform": Platform.PAW_TWICE_DAILY,
        "location": "LIC",
        WEBSITE_RENT_TYPE: RentType.RENTAL,
    },
    {
        WEBSITE_URL_COLUMN: "https://streeteasy.com/building/45_57-davis-street-long_island_city",
        WEBSITE_NAME_COLUMN: "45-57 David St",
        "parent_class_name": "StreetEasy",
        "class_name": "4557DavidSt",
        "platform": Platform.PAW_TWICE_DAILY,
        "location": "LIC",
        WEBSITE_RENT_TYPE: RentType.RENTAL,
    },
    {
        WEBSITE_URL_COLUMN: "https://streeteasy.com/building/halo-lic",
        WEBSITE_NAME_COLUMN: "Halo LIC",
        "parent_class_name": "StreetEasy",
        "class_name": "HaloLIC",
        "platform": Platform.PAW_TWICE_DAILY,
        "location": "LIC",
        WEBSITE_RENT_TYPE: RentType.RENTAL,
    },
    {
        WEBSITE_URL_COLUMN: "https://streeteasy.com/building/trio-27_19-thomson-avenue-long_island_city",
        WEBSITE_NAME_COLUMN: "Trio",
        "parent_class_name": "StreetEasy",
        "class_name": "Trio",
        "platform": Platform.PAW_TWICE_DAILY,
        "location": "LIC",
        WEBSITE_RENT_TYPE: RentType.RENTAL,
    },
    {
        WEBSITE_URL_COLUMN: "https://streeteasy.com/building/skyline-tower",
        WEBSITE_NAME_COLUMN: "Skyline Tower",
        "parent_class_name": "StreetEasy",
        "class_name": "SkylineTower",
        "platform": Platform.PAW_TWICE_DAILY,
        "location": "LIC",
        WEBSITE_RENT_TYPE: RentType.RENTAL,
    },
    {
        WEBSITE_URL_COLUMN: "https://streeteasy.com/building/greene-condominium",
        WEBSITE_NAME_COLUMN: "Greene Condominium",
        "parent_class_name": "StreetEasy",
        "class_name": "GreeneCondominium",
        "platform": Platform.PAW_TWICE_DAILY,
        "location": "LIC",
        WEBSITE_RENT_TYPE: RentType.RENTAL,
    },
    {
        WEBSITE_URL_COLUMN: "https://streeteasy.com/building/the-pearson-court-square",
        WEBSITE_NAME_COLUMN: "Pearson CourtSquare",
        "parent_class_name": "StreetEasy",
        "class_name": "PearsonCourtSquare",
        "platform": Platform.PAW_TWICE_DAILY,
        "location": "LIC",
        WEBSITE_RENT_TYPE: RentType.RENTAL,
    },
    {
        WEBSITE_URL_COLUMN: "https://streeteasy.com/building/the-addition",
        WEBSITE_NAME_COLUMN: "The Addition",
        "class_name": "TheAddition",
        "parent_class_name": "StreetEasy",
        "platform": Platform.PAW_TWICE_DAILY,
        "location": "LIC",
        WEBSITE_RENT_TYPE: RentType.RENTAL,
    },
    {
        WEBSITE_URL_COLUMN: "https://streeteasy.com/building/astor-lic",
        WEBSITE_NAME_COLUMN: "Astor LIC",
        "parent_class_name": "StreetEasy",
        "class_name": "AstorLIC",
        "platform": Platform.PAW_TWICE_DAILY,
        "location": "LIC",
        WEBSITE_RENT_TYPE: RentType.RENTAL,
    },
    {
        WEBSITE_URL_COLUMN: "https://streeteasy.com/building/the-green-house",
        WEBSITE_NAME_COLUMN: "Green House",
        "parent_class_name": "StreetEasy",
        "class_name": "GreenHouse",
        "platform": Platform.PAW_TWICE_DAILY,
        "location": "LIC",
        WEBSITE_RENT_TYPE: RentType.RENTAL,
    },
    {
        WEBSITE_URL_COLUMN: "https://streeteasy.com/complex/gotham-point",
        WEBSITE_NAME_COLUMN: "Gotham Point",
        "parent_class_name": "JacksonParkAWS",
        "class_name": "GothamPoint",
        "platform": Platform.PAW_TWICE_DAILY,
        "location": "LIC",
        WEBSITE_RENT_TYPE: RentType.RENTAL,
    },
    {
        WEBSITE_URL_COLUMN: "https://streeteasy.com/building/47_05-center-blvd-long_island_city",
        WEBSITE_NAME_COLUMN: "RockRose 47-05",
        "parent_class_name": "StreetEasy",
        "class_name": "RockRose4705",
        "platform": Platform.PAW_TWICE_DAILY,
        "location": "LIC",
        WEBSITE_RENT_TYPE: RentType.RENTAL,
    },
    {
        WEBSITE_URL_COLUMN: "https://verisresidential.com/jersey-city-nj-apartments/haus25",
        WEBSITE_NAME_COLUMN: "Haus 25",
        "parent_class_name": "Veris",
        "class_name": "Haus25",
        "platform": Platform.PAW_HOURLY,
        "location": "NJ",
        WEBSITE_RENT_TYPE: RentType.RENTAL,
    },
    {
        WEBSITE_URL_COLUMN: "https://streeteasy.com/building/the-hendrix",
        WEBSITE_NAME_COLUMN: "Hendrix",
        "parent_class_name": "StreetEasy",
        "class_name": "Hendrix",
        "platform": Platform.PAW_TWICE_DAILY,
        "location": "NJ",
        WEBSITE_RENT_TYPE: RentType.RENTAL,
    },
    {
        WEBSITE_URL_COLUMN: "https://www.351marinjc.com/floorplans",
        WEBSITE_NAME_COLUMN: "351 Marin JC",
        "class_name": "351Marinjc",
        "parent_class_name": "981Management",
        "platform": Platform.PAW_HOURLY,
        "location": "NJ",
        WEBSITE_RENT_TYPE: RentType.RENTAL,
    },
    {
        WEBSITE_URL_COLUMN: "https://www.grovepointe.com/floorplans",
        WEBSITE_NAME_COLUMN: "Grove Pointe",
        "class_name": "Gp",
        "parent_class_name": "981Management",
        "platform": Platform.PAW_HALF_HOURLY,
        "location": "NJ",
        WEBSITE_RENT_TYPE: RentType.RENTAL,
    },
    {
        WEBSITE_URL_COLUMN: "https://www.235grand.com/floorplans",
        WEBSITE_NAME_COLUMN: "235 Grand Street",
        "class_name": "235GrandStreet",
        "parent_class_name": "981Management",
        "platform": Platform.PAW_HALF_HOURLY,
        "location": "NJ",
        WEBSITE_RENT_TYPE: RentType.RENTAL,
    },
    {
        WEBSITE_URL_COLUMN: "https://ironstate.com/property/90-columbus",
        WEBSITE_NAME_COLUMN: "90 Columbus",
        "parent_class_name": "IronState",
        "class_name": "90Columbus",
        "platform": Platform.PAW_HALF_HOURLY,
        "location": "NJ",
        WEBSITE_RENT_TYPE: RentType.RENTAL,
    },
    {
        WEBSITE_URL_COLUMN: "https://ironstate.com/property/70-columbus",
        WEBSITE_NAME_COLUMN: "70 Columbus",
        "parent_class_name": "IronState",
        "class_name": "70Columbus",
        "platform": Platform.PAW_HALF_HOURLY,
        "location": "NJ",
        WEBSITE_RENT_TYPE: RentType.RENTAL,
    },
    {
        WEBSITE_URL_COLUMN: "https://ironstate.com/property/50-columbus",
        WEBSITE_NAME_COLUMN: "50 Columbus",
        "parent_class_name": "IronState",
        "class_name": "50Columbus",
        "platform": Platform.PAW_HALF_HOURLY,
        "location": "NJ",
        WEBSITE_RENT_TYPE: RentType.RENTAL,
    },
    {
        WEBSITE_URL_COLUMN: "https://ironstate.com/property/the-gotham",
        WEBSITE_NAME_COLUMN: "The Gotham",
        "parent_class_name": "IronState",
        "class_name": "TheGotham",
        "platform": Platform.PAW_HALF_HOURLY,
        "location": "NJ",
        WEBSITE_RENT_TYPE: RentType.RENTAL,
    },
    {
        WEBSITE_URL_COLUMN: "https://www.225grandstreet.com/floorplans",
        WEBSITE_NAME_COLUMN: "225 Grand Street",
        "class_name": "225GrandStreet",
        "parent_class_name": "981Management",
        "platform": Platform.PAW_HALF_HOURLY,
        "location": "NJ",
        WEBSITE_RENT_TYPE: RentType.RENTAL,
    },
    {
        WEBSITE_URL_COLUMN: "https://www.18park.com/floorplans",
        WEBSITE_NAME_COLUMN: "18 Park",
        "class_name": "18Park",
        "parent_class_name": "981Management",
        "platform": Platform.PAW_HALF_HOURLY,
        "location": "NJ",
        WEBSITE_RENT_TYPE: RentType.RENTAL,
    },
    {
        WEBSITE_URL_COLUMN: "https://ironstate.com/property/340-third",
        WEBSITE_NAME_COLUMN: "340 Third",
        "parent_class_name": "IronState",
        "class_name": "340Third",
        "platform": Platform.PAW_HOURLY,
        "location": "NJ",
        WEBSITE_RENT_TYPE: RentType.RENTAL,
    },
    {
        WEBSITE_URL_COLUMN: "https://www.485marin.com/floorplans",
        WEBSITE_NAME_COLUMN: "485 Marin",
        "class_name": "485Marin",
        "parent_class_name": "981Management",
        "platform": Platform.PAW_HOURLY,
        "location": "NJ",
        WEBSITE_RENT_TYPE: RentType.RENTAL,
    },
    {
        WEBSITE_URL_COLUMN: "https://www.livethemorgan.com/floor-plans",
        WEBSITE_NAME_COLUMN: "Live The Morgan",
        "class_name": "LiveTheMorgan",
        "platform": Platform.PAW_HOURLY,
        "location": "NJ",
        WEBSITE_RENT_TYPE: RentType.RENTAL,
    },
    {
        WEBSITE_URL_COLUMN: "https://www.urby.com/location/jersey-city/availability",
        WEBSITE_NAME_COLUMN: "JC Urby",
        "parent_class_name": "Urby",
        "class_name": "JCUrby",
        "platform": Platform.PAW_HOURLY,
        "location": "NJ",
        WEBSITE_RENT_TYPE: RentType.RENTAL,
    },
    {
        WEBSITE_URL_COLUMN: "https://streeteasy.com/building/88-regent-street-jersey_city",
        WEBSITE_NAME_COLUMN: "88 Regent",
        "parent_class_name": "StreetEasy",
        "class_name": "88Regent",
        "platform": Platform.PAW_TWICE_DAILY,
        "location": "NJ",
        WEBSITE_RENT_TYPE: RentType.RENTAL,
    },
    {
        WEBSITE_URL_COLUMN: "https://streeteasy.com/building/the-bridget",
        WEBSITE_NAME_COLUMN: "The Bridget",
        "parent_class_name": "StreetEasy",
        "class_name": "TheBridget",
        "platform": Platform.PAW_TWICE_DAILY,
        "location": "NJ",
        WEBSITE_RENT_TYPE: RentType.RENTAL,
    },
    {
        WEBSITE_URL_COLUMN: "https://streeteasy.com/building/quinn-197-van-vorst-street-jersey_city",
        WEBSITE_NAME_COLUMN: "Quinn",
        "parent_class_name": "StreetEasy",
        "class_name": "Quinn",
        "platform": Platform.PAW_TWICE_DAILY,
        "location": "NJ",
        WEBSITE_RENT_TYPE: RentType.RENTAL,
    },
    {
        WEBSITE_URL_COLUMN: "https://dvoralife.com/buildings/art-house",
        WEBSITE_NAME_COLUMN: "Art House",
        "parent_class_name": "Dvora",
        "class_name": "ArtHouse",
        "platform": Platform.PAW_HOURLY,
        "location": "NJ",
        WEBSITE_RENT_TYPE: RentType.RENTAL,
    },
    {
        WEBSITE_URL_COLUMN: "https://dvoralife.com/buildings/175-second",
        WEBSITE_NAME_COLUMN: "175 Second",
        "parent_class_name": "Dvora",
        "class_name": "175Second",
        "platform": Platform.PAW_HOURLY,
        "location": "NJ",
        WEBSITE_RENT_TYPE: RentType.RENTAL,
    },
    {
        WEBSITE_URL_COLUMN: "https://dvoralife.com/buildings/109-columbus",
        WEBSITE_NAME_COLUMN: "109 Columbus Dr",
        "parent_class_name": "Dvora",
        "class_name": "109ColumbusDr",
        "platform": Platform.PAW_HOURLY,
        "location": "NJ",
        WEBSITE_RENT_TYPE: RentType.RENTAL,
    },
    {
        WEBSITE_URL_COLUMN: "https://streeteasy.com/building/vantage-33-park-view-avenue-jersey_city",
        WEBSITE_NAME_COLUMN: "Vantage",
        "parent_class_name": "StreetEasy",
        "class_name": "Vantage",
        "platform": Platform.PAW_TWICE_DAILY,
        "location": "NJ",
        WEBSITE_RENT_TYPE: RentType.RENTAL,
    },
    {
        WEBSITE_URL_COLUMN: "https://ironstate.com/property/le-leo",
        WEBSITE_NAME_COLUMN: "Le Leo",
        "parent_class_name": "IronState",
        "class_name": "LeLeo",
        "platform": Platform.PAW_HOURLY,
        "location": "NJ",
        WEBSITE_RENT_TYPE: RentType.RENTAL,
    },
    {
        WEBSITE_URL_COLUMN: "https://www.urby.com/location/journal-square/availability",
        WEBSITE_NAME_COLUMN: "Journal Square Urby",
        "parent_class_name": "Urby",
        "class_name": "JournalSquareUrby",
        "platform": Platform.PAW_HOURLY,
        "location": "NJ",
        WEBSITE_RENT_TYPE: RentType.RENTAL,
    },
    {
        WEBSITE_URL_COLUMN: "https://streeteasy.com/building/55-jordan-avenue-jersey_city",
        WEBSITE_NAME_COLUMN: "55 Jordan",
        "parent_class_name": "StreetEasy",
        "class_name": "55Jordan",
        "platform": Platform.PAW_TWICE_DAILY,
        "location": "NJ",
        WEBSITE_RENT_TYPE: RentType.RENTAL,
    },
    {
        WEBSITE_URL_COLUMN: "https://www.journalsquared.com/availabilities",
        WEBSITE_NAME_COLUMN: "Journal Squared",
        "class_name": "Jsq",
        "platform": Platform.PAW_HOURLY,
        "location": "NJ",
        WEBSITE_RENT_TYPE: RentType.RENTAL,
    },
    {
        WEBSITE_URL_COLUMN: "https://www.65bay.com/floorplans.aspx",
        WEBSITE_NAME_COLUMN: "65 Bay",
        "class_name": "65Bay",
        "platform": Platform.PAW_HOURLY,
        "location": "NJ2",
        WEBSITE_RENT_TYPE: RentType.RENTAL,
    },
    # {
    #     WEBSITE_URL_COLUMN: "https://www.vyvapts.com/availability",
    #     WEBSITE_NAME_COLUMN: "VYV",
    #     "class_name": "VYV",
    #     "platform": Platform.PAW_HOURLY,
    #     "location": "NJ2",
    #     WEBSITE_RENT_TYPE: RentType.RENTAL,
    # },
    {
        WEBSITE_URL_COLUMN: "https://www.urby.com/location/harrison/availability",
        WEBSITE_NAME_COLUMN: "Harrison Urby",
        "parent_class_name": "Urby",
        "class_name": "HarrisonUrby",
        "platform": Platform.PAW_HOURLY,
        "location": "NJ2",
        WEBSITE_RENT_TYPE: RentType.RENTAL,
    },
    {
        WEBSITE_URL_COLUMN: "https://www.newportrentals.com/apartments-jersey-city-for-rent/",
        WEBSITE_NAME_COLUMN: "Newport Rental",
        "class_name": "NewportRental",
        "platform": Platform.PAW_HOURLY,
        "location": "NPR",
        WEBSITE_RENT_TYPE: RentType.RENTAL,
    },
    {
        WEBSITE_URL_COLUMN: "https://www.avaloncommunities.com/new-york/new-york-city-apartments/avalon-morningside-park",
        WEBSITE_NAME_COLUMN: "Avalon MorningSide Park",
        "parent_class_name": "Avalon",
        "class_name": "AvalonMorningSidePark",
        "platform": Platform.PAW_HOURLY,
        "location": "CU",
        WEBSITE_RENT_TYPE: RentType.RENTAL,
    },
    {
        WEBSITE_URL_COLUMN: "https://streeteasy.com/building/792-columbus-avenue-new_york",
        WEBSITE_NAME_COLUMN: "PWV",
        "parent_class_name": "StreetEasy",
        "class_name": "PWV",
        "platform": Platform.PAW_TWICE_DAILY,
        "location": "CU",
        WEBSITE_RENT_TYPE: RentType.RENTAL,
    },
    {
        WEBSITE_URL_COLUMN: "https://streeteasy.com/building/323-west-96-street-new_york",
        WEBSITE_NAME_COLUMN: "Hudson Park",
        "parent_class_name": "StreetEasy",
        "class_name": "HudsonPark",
        "platform": Platform.PAW_TWICE_DAILY,
        "location": "CU",
        WEBSITE_RENT_TYPE: RentType.RENTAL,
    },
    {
        WEBSITE_URL_COLUMN: "https://streeteasy.com/building/windermere-666-west-end-avenue-new_york",
        WEBSITE_NAME_COLUMN: "Windermere",
        "parent_class_name": "StreetEasy",
        "class_name": "Windermere",
        "platform": Platform.PAW_TWICE_DAILY,
        "location": "CU",
        WEBSITE_RENT_TYPE: RentType.RENTAL,
    },
    {
        WEBSITE_URL_COLUMN: "https://streeteasy.com/building/the-melar",
        WEBSITE_NAME_COLUMN: "The Melar",
        "parent_class_name": "StreetEasy",
        "class_name": "TheMelar",
        "platform": Platform.PAW_TWICE_DAILY,
        "location": "CU",
        WEBSITE_RENT_TYPE: RentType.RENTAL,
    },
    {
        WEBSITE_URL_COLUMN: "https://streeteasy.com/building/the-greystone",
        WEBSITE_NAME_COLUMN: "Greystone",
        "parent_class_name": "StreetEasy",
        "class_name": "Greystone",
        "platform": Platform.PAW_TWICE_DAILY,
        "location": "CU",
        WEBSITE_RENT_TYPE: RentType.RENTAL,
    },
    {
        WEBSITE_URL_COLUMN: "https://tfc.com/new-york-luxury-no-fee-apartments/plaza-district--lincoln-square--midtown-south--union-square--williamsburg-brooklyn--penn-quarter--golden-triangle--midtown--meatpacking-district--nomad--astoria--hudson-yards--greenwich-village--bushwick--prospect-heights--chelsea--washington-dc--flatiron--midtown-east--gramercy-park--reston-rentals",
        WEBSITE_NAME_COLUMN: "TFC Chelsea",
        "parent_class_name": "TFC",
        "class_name": "TFCChelsea",
        "platform": Platform.PAW_HOURLY,
        "location": "TFCChelsea",
        WEBSITE_RENT_TYPE: RentType.RENTAL,
    },
    {
        WEBSITE_URL_COLUMN: "https://tfc.com/new-york-luxury-no-fee-apartments/plaza-district--lincoln-square--midtown-south--union-square--williamsburg-brooklyn--penn-quarter--golden-triangle--midtown--meatpacking-district--nomad--astoria--west-village--financial-district--long-island-city--greenwich-village--downtown-brooklyn--bushwick--murray-hill--midtown-west--prospect-heights--upper-east-side--washington-dc--flatiron--midtown-east--gramercy-park--reston-rentals",
        WEBSITE_NAME_COLUMN: "TFC Others",
        "parent_class_name": "TFC",
        "class_name": "TFCOthers",
        "platform": Platform.PAW_HOURLY,
        "location": "TFCOthers",
        WEBSITE_RENT_TYPE: RentType.RENTAL,
    },
    {
        WEBSITE_URL_COLUMN: "https://streeteasy.com/building/88_08-justice-avenue-elmhurst_",
        WEBSITE_NAME_COLUMN: "88-08 Justice Ave",
        "parent_class_name": "StreetEasy",
        "class_name": "JusticeAve",
        "platform": Platform.PAW_TWICE_DAILY,
        "location": "Elmhurst",
        WEBSITE_RENT_TYPE: RentType.RENTAL,
    },
    {
        WEBSITE_URL_COLUMN: "https://streeteasy.com/building/the-alexander-61_55-junction-boulevard-rego_park",
        WEBSITE_NAME_COLUMN: "Alexander",
        "parent_class_name": "StreetEasy",
        "class_name": "Alexander",
        "platform": Platform.PAW_TWICE_DAILY,
        "location": "Elmhurst",
        WEBSITE_RENT_TYPE: RentType.RENTAL,
    },
    {
        WEBSITE_URL_COLUMN: "https://streeteasy.com/building/181-front-street",
        WEBSITE_NAME_COLUMN: "181 Front",
        "parent_class_name": "StreetEasy",
        "class_name": "181Front",
        "platform": Platform.PAW_TWICE_DAILY,
        "location": "BK",
        WEBSITE_RENT_TYPE: RentType.RENTAL,
    },
    {
        WEBSITE_URL_COLUMN: "https://streeteasy.com/building/the-amberly",
        WEBSITE_NAME_COLUMN: "The Amberly",
        "parent_class_name": "StreetEasy",
        "class_name": "TheAmberly",
        "platform": Platform.PAW_TWICE_DAILY,
        "location": "BK",
        WEBSITE_RENT_TYPE: RentType.RENTAL,
    },
    {
        WEBSITE_URL_COLUMN: "https://streeteasy.com/building/22-chapel-street-brooklyn",
        WEBSITE_NAME_COLUMN: "22 Chapel",
        "parent_class_name": "StreetEasy",
        "class_name": "22Chapel",
        "platform": Platform.PAW_TWICE_DAILY,
        "location": "BK",
        WEBSITE_RENT_TYPE: RentType.RENTAL,
    },
    {
        WEBSITE_URL_COLUMN: "https://streeteasy.com/building/260-gold",
        WEBSITE_NAME_COLUMN: "260 Gold St",
        "parent_class_name": "StreetEasy",
        "class_name": "260GoldSt",
        "platform": Platform.PAW_TWICE_DAILY,
        "location": "BK",
        WEBSITE_RENT_TYPE: RentType.RENTAL,
    },
    {
        WEBSITE_URL_COLUMN: "https://streeteasy.com/building/200-montague-street-brooklyn",
        WEBSITE_NAME_COLUMN: "200 Montague St",
        "parent_class_name": "StreetEasy",
        "class_name": "200MontagueSt",
        "platform": Platform.PAW_TWICE_DAILY,
        "location": "BK",
        WEBSITE_RENT_TYPE: RentType.RENTAL,
    },
    {
        WEBSITE_URL_COLUMN: "https://www.avaloncommunities.com/new-york/brooklyn-apartments/ava-fort-greene",
        WEBSITE_NAME_COLUMN: "Ava Fort Greene",
        "parent_class_name": "Avalon",
        "class_name": "AvaFortGreene",
        "platform": Platform.PAW_HOURLY,
        "location": "BK",
        WEBSITE_RENT_TYPE: RentType.RENTAL,
    },
    {
        WEBSITE_URL_COLUMN: "https://streeteasy.com/building/the-brooklyner",
        WEBSITE_NAME_COLUMN: "The Brooklyner",
        "parent_class_name": "StreetEasy",
        "class_name": "TheBrooklyner",
        "platform": Platform.PAW_TWICE_DAILY,
        "location": "BK",
        WEBSITE_RENT_TYPE: RentType.RENTAL,
    },
    {
        WEBSITE_URL_COLUMN: "https://www.avaloncommunities.com/new-york/brooklyn-apartments/ava-dobro",
        WEBSITE_NAME_COLUMN: "Ava DoBro",
        "parent_class_name": "Avalon",
        "class_name": "AvaDoBro",
        "platform": Platform.PAW_HOURLY,
        "location": "BK",
        WEBSITE_RENT_TYPE: RentType.RENTAL,
    },
    {
        WEBSITE_URL_COLUMN: "https://streeteasy.com/building/city-tower",
        WEBSITE_NAME_COLUMN: "City Tower",
        "parent_class_name": "StreetEasy",
        "class_name": "CityTower",
        "platform": Platform.PAW_TWICE_DAILY,
        "location": "BK",
        WEBSITE_RENT_TYPE: RentType.RENTAL,
    },
    {
        WEBSITE_URL_COLUMN: "https://streeteasy.com/building/the-azure-436-albee-square",
        WEBSITE_NAME_COLUMN: "The Azure",
        "parent_class_name": "StreetEasy",
        "class_name": "TheAzure",
        "platform": Platform.PAW_TWICE_DAILY,
        "location": "BK",
        WEBSITE_RENT_TYPE: RentType.RENTAL,
    },
    {
        WEBSITE_URL_COLUMN: "https://streeteasy.com/building/the-eagle",
        WEBSITE_NAME_COLUMN: "The Eagle",
        "parent_class_name": "StreetEasy",
        "class_name": "TheEagle",
        "platform": Platform.PAW_TWICE_DAILY,
        "location": "BK",
        WEBSITE_RENT_TYPE: RentType.RENTAL,
    },
    {
        WEBSITE_URL_COLUMN: "https://streeteasy.com/building/willoughby-196-willoughby-street-brooklyn___",
        WEBSITE_NAME_COLUMN: "The Willoughby",
        "parent_class_name": "StreetEasy",
        "class_name": "TheWilloughby",
        "platform": Platform.PAW_TWICE_DAILY,
        "location": "BK",
        WEBSITE_RENT_TYPE: RentType.RENTAL,
    },
    {
        WEBSITE_URL_COLUMN: "https://streeteasy.com/building/hoyt-and-horn",
        WEBSITE_NAME_COLUMN: "Hoyt and Horn",
        "parent_class_name": "StreetEasy",
        "class_name": "HoytAndHorn",
        "platform": Platform.PAW_TWICE_DAILY,
        "location": "BK",
        WEBSITE_RENT_TYPE: RentType.RENTAL,
    },
    {
        WEBSITE_URL_COLUMN: "https://streeteasy.com/building/33-bond-street-brooklyn",
        WEBSITE_NAME_COLUMN: "33 Bond",
        "parent_class_name": "StreetEasy",
        "class_name": "33Bond",
        "platform": Platform.PAW_TWICE_DAILY,
        "location": "BK",
        WEBSITE_RENT_TYPE: RentType.RENTAL,
    },
    {
        WEBSITE_URL_COLUMN: "https://streeteasy.com/building/the-guild",
        WEBSITE_NAME_COLUMN: "The Guild",
        "parent_class_name": "StreetEasy",
        "class_name": "TheGuild",
        "platform": Platform.PAW_TWICE_DAILY,
        "location": "BK",
        WEBSITE_RENT_TYPE: RentType.RENTAL,
    },
    {
        WEBSITE_URL_COLUMN: "https://streeteasy.com/building/hub-333-schermerhorn-street-brooklyn",
        WEBSITE_NAME_COLUMN: "Hub",
        "parent_class_name": "StreetEasy",
        "class_name": "Hub",
        "platform": Platform.PAW_TWICE_DAILY,
        "location": "BK",
        WEBSITE_RENT_TYPE: RentType.RENTAL,
    },
    {
        WEBSITE_URL_COLUMN: "https://streeteasy.com/building/the-addison-brooklyn",
        WEBSITE_NAME_COLUMN: "The Addison",
        "parent_class_name": "StreetEasy",
        "class_name": "TheAddison",
        "platform": Platform.PAW_TWICE_DAILY,
        "location": "BK",
        WEBSITE_RENT_TYPE: RentType.RENTAL,
    },
    {
        WEBSITE_URL_COLUMN: "https://streeteasy.com/building/plank-road",
        WEBSITE_NAME_COLUMN: "Plank Road",
        "parent_class_name": "StreetEasy",
        "class_name": "PlankRoad",
        "platform": Platform.PAW_TWICE_DAILY,
        "location": "BK",
        WEBSITE_RENT_TYPE: RentType.RENTAL,
    },
    {
        WEBSITE_URL_COLUMN: "https://streeteasy.com/building/475-clermont",
        WEBSITE_NAME_COLUMN: "475 Clermont",
        "parent_class_name": "StreetEasy",
        "class_name": "475Clermont",
        "platform": Platform.PAW_TWICE_DAILY,
        "location": "BK",
        WEBSITE_RENT_TYPE: RentType.RENTAL,
    },
    {
        WEBSITE_URL_COLUMN: "https://streeteasy.com/building/brooklyn-crossing",
        WEBSITE_NAME_COLUMN: "BK Crossing",
        "parent_class_name": "StreetEasy",
        "class_name": "BkCrosing",
        "platform": Platform.PAW_TWICE_DAILY,
        "location": "BK",
        WEBSITE_RENT_TYPE: RentType.RENTAL,
    },
    {
        WEBSITE_URL_COLUMN: "https://streeteasy.com/building/the-posthouse",
        WEBSITE_NAME_COLUMN: "The Posthouse",
        "parent_class_name": "StreetEasy",
        "class_name": "ThePosthouse",
        "platform": Platform.PAW_TWICE_DAILY,
        "location": "BK",
        WEBSITE_RENT_TYPE: RentType.RENTAL,
    },
    {
        WEBSITE_URL_COLUMN: "https://streeteasy.com/building/the-axel",
        WEBSITE_NAME_COLUMN: "The Axel",
        "parent_class_name": "StreetEasy",
        "class_name": "TheAxel",
        "platform": Platform.PAW_TWICE_DAILY,
        "location": "BK",
        WEBSITE_RENT_TYPE: RentType.RENTAL,
    },
    {
        WEBSITE_URL_COLUMN: "https://streeteasy.com/building/180-franklin-avenue-brooklyn",
        WEBSITE_NAME_COLUMN: "180 Franklin",
        "parent_class_name": "StreetEasy",
        "class_name": "180Franklin",
        "platform": Platform.PAW_TWICE_DAILY,
        "location": "BK",
        WEBSITE_RENT_TYPE: RentType.RENTAL,
    },
    {
        WEBSITE_URL_COLUMN: "https://streeteasy.com/complex/myrtle-steuben",
        WEBSITE_NAME_COLUMN: "Myrtle Steuben",
        "class_name": "MyrtleSteuben",
        "platform": Platform.PAW_TWICE_DAILY,
        "location": "BK",
        WEBSITE_RENT_TYPE: RentType.RENTAL,
    },
    {
        WEBSITE_URL_COLUMN: "https://streeteasy.com/building/325-lafayette-avenue-brooklyn",
        WEBSITE_NAME_COLUMN: "325 Lafayette",
        "parent_class_name": "StreetEasy",
        "class_name": "325Lafayette",
        "platform": Platform.PAW_TWICE_DAILY,
        "location": "BK",
        WEBSITE_RENT_TYPE: RentType.RENTAL,
    },
    {
        WEBSITE_URL_COLUMN: "https://streeteasy.com/building/540-waverly-avenue-brooklyn",
        WEBSITE_NAME_COLUMN: "540 Waverly Ave",
        "parent_class_name": "StreetEasy",
        "class_name": "540WaverlyAve",
        "platform": Platform.PAW_TWICE_DAILY,
        "location": "BKLow",
        WEBSITE_RENT_TYPE: RentType.RENTAL,
    },
    {
        WEBSITE_URL_COLUMN: "https://streeteasy.com/building/1134-fulton-street-brooklyn",
        WEBSITE_NAME_COLUMN: "1134 Fulton St",
        "parent_class_name": "StreetEasy",
        "class_name": "1134FultonSt",
        "platform": Platform.PAW_TWICE_DAILY,
        "location": "BKLow",
        WEBSITE_RENT_TYPE: RentType.RENTAL,
    },
    {
        WEBSITE_URL_COLUMN: "https://streeteasy.com/building/11-herkimer",
        WEBSITE_NAME_COLUMN: "11 Herkimer",
        "parent_class_name": "StreetEasy",
        "class_name": "11Herkimer",
        "platform": Platform.PAW_TWICE_DAILY,
        "location": "BKLow",
        WEBSITE_RENT_TYPE: RentType.RENTAL,
    },
    {
        WEBSITE_URL_COLUMN: "https://streeteasy.com/building/fulton-crossing",
        WEBSITE_NAME_COLUMN: "1430 Fulton Street",
        "parent_class_name": "StreetEasy",
        "class_name": "1430FultonStreet",
        "platform": Platform.PAW_TWICE_DAILY,
        "location": "BKLow",
        WEBSITE_RENT_TYPE: RentType.RENTAL,
    },
    {
        WEBSITE_URL_COLUMN: "https://www.ehomie.com/us/new-york/region-10004/apartment/e03s2",
        WEBSITE_NAME_COLUMN: "Ehomie LIC Queen",
        "parent_class_name": "Ehomie",
        "class_name": "EhomieLICQueen",
        "platform": Platform.PAW_HOURLY,
        "location": "LIC Queen",
        WEBSITE_RENT_TYPE: RentType.SUBLEASE,
    },
    {
        WEBSITE_URL_COLUMN: "https://www.ehomie.com/us/new-york/region-10001/apartment/e03s2",
        WEBSITE_NAME_COLUMN: "Ehomie Mid Manhattan",
        "parent_class_name": "Ehomie",
        "class_name": "EhomieMidMan",
        "platform": Platform.PAW_HOURLY,
        "location": "Mid Manhattan",
        WEBSITE_RENT_TYPE: RentType.SUBLEASE,
    },
    {
        WEBSITE_URL_COLUMN: "https://www.ehomie.com/us/new-york/region-10002/apartment/e03s2",
        WEBSITE_NAME_COLUMN: "Ehomie Up Manhattan",
        "parent_class_name": "Ehomie",
        "class_name": "EhomieUpMan",
        "platform": Platform.PAW_HOURLY,
        "location": "Up Manhattan",
        WEBSITE_RENT_TYPE: RentType.SUBLEASE,
    },
    {
        WEBSITE_URL_COLUMN: "https://www.ehomie.com/us/new-york/region-10003/apartment/e03s2",
        WEBSITE_NAME_COLUMN: "Ehomie NJ",
        "parent_class_name": "Ehomie",
        "class_name": "EhomieNJ",
        "platform": Platform.PAW_HOURLY,
        "location": "NJ",
        WEBSITE_RENT_TYPE: RentType.SUBLEASE,
    },
    {
        WEBSITE_URL_COLUMN: "https://www.ehomie.com/us/new-york/region-10005/apartment/e03s2",
        WEBSITE_NAME_COLUMN: "Ehomie Brooklyn",
        "parent_class_name": "Ehomie",
        "class_name": "EhomieBK",
        "platform": Platform.PAW_HOURLY,
        "location": "Brooklyn",
        WEBSITE_RENT_TYPE: RentType.SUBLEASE,
    },
    {
        WEBSITE_URL_COLUMN: "https://www.ehomie.com/us/new-york/region-10006/apartment/e03s2",
        WEBSITE_NAME_COLUMN: "Ehomie Roosevelt",
        "parent_class_name": "Ehomie",
        "class_name": "EhomieRoosevelt",
        "platform": Platform.PAW_HOURLY,
        "location": "Roosevelt",
        WEBSITE_RENT_TYPE: RentType.SUBLEASE,
    },
    {
        WEBSITE_URL_COLUMN: "https://streeteasy.com/building/aro-242-west-53-street-new_york",
        WEBSITE_NAME_COLUMN: "Aro",
        "parent_class_name": "StreetEasy",
        "class_name": "Aro",
        "platform": Platform.PAW_TWICE_DAILY,
        "location": "Manhattan",
        WEBSITE_RENT_TYPE: RentType.RENTAL,
    },
    {
        WEBSITE_URL_COLUMN: "https://streeteasy.com/building/the-copper",
        WEBSITE_NAME_COLUMN: "The Copper",
        "parent_class_name": "StreetEasy",
        "class_name": "TheCopper",
        "platform": Platform.PAW_TWICE_DAILY,
        "location": "Manhattan",
        WEBSITE_RENT_TYPE: RentType.RENTAL,
    },
    {
        WEBSITE_URL_COLUMN: "https://streeteasy.com/building/685-first-avenue-manhattan",
        WEBSITE_NAME_COLUMN: "685 First Avenue",
        "parent_class_name": "StreetEasy",
        "class_name": "685FirstAvenue",
        "platform": Platform.PAW_TWICE_DAILY,
        "location": "Manhattan",
        WEBSITE_RENT_TYPE: RentType.RENTAL,
    },
    {
        WEBSITE_URL_COLUMN: "https://verisresidential.com/jersey-city-nj-apartments/the-blvd-collection",
        WEBSITE_NAME_COLUMN: "The Blvd",
        "parent_class_name": "Veris",
        "class_name": "TheBlvd",
        "platform": Platform.PAW_HOURLY,
        "location": "NJ",
        WEBSITE_RENT_TYPE: RentType.RENTAL,
    },
]


WEBSITES_DICT = {
    website["class_name"]: {**website, WEBSITE_PRIORITY_COLUMN: index}
    for index, website in enumerate(WEBSITES)
}

NOTIFICATION_EMAIL_SUBJECT = "【房源通知】"
NOTIFICATION_EMAIL_SUBJECT_SUMMER_SUMMARY = "【暑期新房源通知】"
SNAPSHOT_EMAIL_SUBJECT = "【房源每日快照】"
ERROR_EMAIL_SUBJECT = "【房源抓取出错了】"
EMAIL_SENDER = "rent.spider.notification@gmail.com"
EMAIL_RECEIVERS_DEV = ["ppttzhu@gmail.com"]
EMAIL_RECEIVERS = ["Newyorkrental@163.com"]
SNAPSHOT_EMAIL_RECEIVERS = ["Newyorkrental@163.com"]
TOP_5_EXCLUDE = [
    "Pearson CourtSquare",
    "Dutch House",
    "Bevel LIC",
    "Packard Square",
    "Packard Square West",
    "45-57 David St",
    "Halo LIC",
    "The Bridget",
    "Art House",
    "175 Second",
    "109 Columbus Dr",
    "55 Jordan",
]


DATABASE_HOST = "ppttzhu.mysql.pythonanywhere-services.com"
DATABASE_USER = "ppttzhu"
DATABASE_NAME = "ppttzhu$default"

WEB_APP_LINK = "https://ppttzhu.pythonanywhere.com"

SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 587

SSH_HOST = "ssh.pythonanywhere.com"
SSH_USERNAME = "ppttzhu"
SSH_REMOTE_BIND_ADDRESS = "ppttzhu.mysql.pythonanywhere-services.com"
SSH_REMOTE_BIND_PORT = 3306

# Parse argument
try:
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--include", nargs="+", help="Websites to include")
    parser.add_argument("-e", "--exclude", nargs="+", help="Websites to exclude")
    parser.add_argument("-p", "--platform", help="Platform to select")
    parser.add_argument(
        "-s", "--sublease", action="store_true", help="Sublease websites only"
    )
    parser.add_argument(
        "-r", "--remote", action="store_true", help="SSH to remote database"
    )
    parser.add_argument(
        "-u", "--update", action="store_true", help="Update website table"
    )
    args = parser.parse_args()

    PLATFORM = Platform[args.platform] if args.platform else Platform.DEV
    IS_REMOTE = args.remote

    NEED_UPDATE_WEBSITE = args.update
    RENT_TYPE = RentType.SUBLEASE if args.sublease else RentType.RENTAL

    if args.include:
        WEBSITES_TARGETS = args.include
    elif args.exclude:
        WEBSITES_TARGETS = list(
            filter(lambda x: x not in args.exclude, WEBSITES_DICT.keys())
        )
    elif args.sublease:
        website_for_sublease = list(
            filter(lambda x: x[WEBSITE_RENT_TYPE] == RentType.SUBLEASE, WEBSITES)
        )
        WEBSITES_TARGETS = [w["class_name"] for w in website_for_sublease]
    elif PLATFORM != Platform.DEV:
        website_for_platform = list(
            filter(
                lambda x: x["platform"] == PLATFORM
                and x[WEBSITE_RENT_TYPE] != RentType.SUBLEASE,
                WEBSITES,
            )
        )
        WEBSITES_TARGETS = [w["class_name"] for w in website_for_platform]
    else:
        WEBSITES_TARGETS = WEBSITES_DICT.keys()
except Exception:
    WEBSITES_TARGETS = WEBSITES_DICT.keys()
