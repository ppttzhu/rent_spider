import argparse
import os
from enum import Enum


class Platform(Enum):
    AWS = 1
    PYTHONANYWHERE = 2
    DEV = 3


class RentType(Enum):
    RENTAL = 1
    SUBLEASE = 2


PLATFORM = None
NEED_UPDATE_WEBSITE = None
WEBSITES_TARGETS = None

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

MINUTES_BETWEEN_FETCH = 7
TOTAL_DURATION_IN_MINUTES = 55
WEB_DRIVER_WAIT_SECOND = 20


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
ROOM_TYPE_COLUMN = "room_type"
MOVE_IN_DATE_COLUMN = "move_in_date"
ROOM_PRICE_COLUMN = "room_price"
FETCH_DATE_COLUMN = "fetch_date"
ROOM_COUNT_COLUMN = "room_count"
ROOM_TITLE_COLUMN = "room_title"
ROOM_URL_COLUMN = "room_url"
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
SUBLEASE_TABLE_COLUMNS_NAME = ["房源网站", "转租信息", "户型", "入住时间", "房价", "发布时间"]
FETCH_DATE_COLUMN_NAME = "抓取时间"
ROOM_COUNT_COLUMN_NAME = "房间数量"
FETCH_STATUS_COLUMNS_NAME = ["房源网站", ROOM_COUNT_COLUMN_NAME, FETCH_DATE_COLUMN_NAME]

WEBSITE_ROOM_VIEW_NAME = "v_website_room"
WEBSITE_SUBLEASE_VIEW_NAME = "v_website_sublease"
WEBSITE_ROOM_HISTORY_VIEW_NAME = "v_website_room_history"
FETCH_STATUS_VIEW_NAME = "v_fetch_status"
WEBSITE_ROOM_VIEW_ADDITIONAL_COLUMNS = [
    WEBSITE_URL_COLUMN,
    WEBSITE_LOCATION_COLUMN,
    WEBSITE_PRIORITY_COLUMN,
]
WEBSITE_ROOM_VIEW_COLUMNS = ROOM_TABLE_COLUMNS + WEBSITE_ROOM_VIEW_ADDITIONAL_COLUMNS
WEBSITE_SUBLEASE_VIEW_COLUMNS = SUBLEASE_TABLE_COLUMNS + WEBSITE_ROOM_VIEW_ADDITIONAL_COLUMNS

WEBSITES = [
    {
        WEBSITE_URL_COLUMN: "https://streeteasy.com/building/steel-haus",
        WEBSITE_NAME_COLUMN: "Steel Haus",
        "class_name": "SteelHaus",
        "platform": Platform.AWS,
        "location": "LIC",
        WEBSITE_RENT_TYPE: RentType.RENTAL,
    },
    {
        WEBSITE_URL_COLUMN: "https://jacksonparklic.com/availability/",
        WEBSITE_NAME_COLUMN: "Jackson Park LIC",
        "class_name": "JacksonPark",
        "platform": Platform.PYTHONANYWHERE,
        "location": "LIC",
        WEBSITE_RENT_TYPE: RentType.RENTAL,
    },
    {
        WEBSITE_URL_COLUMN: "https://streeteasy.com/complex/jackson-park-lic",
        WEBSITE_NAME_COLUMN: "Jackson Park LIC SE",
        "class_name": "JacksonParkAWS",
        "platform": Platform.AWS,
        "location": "LIC",
        WEBSITE_RENT_TYPE: RentType.RENTAL,
    },
    {
        WEBSITE_URL_COLUMN: "https://streeteasy.com/building/1-qps",
        WEBSITE_NAME_COLUMN: "1 QPS",
        "class_name": "1QPS",
        "platform": Platform.AWS,
        "location": "LIC",
        WEBSITE_RENT_TYPE: RentType.RENTAL,
    },
    {
        WEBSITE_URL_COLUMN: "https://streeteasy.com/building/rise-lic",
        WEBSITE_NAME_COLUMN: "Rise LIC",
        "class_name": "RiseLIC",
        "platform": Platform.AWS,
        "location": "LIC",
        WEBSITE_RENT_TYPE: RentType.RENTAL,
    },
    {
        WEBSITE_URL_COLUMN: "https://streeteasy.com/building/skyline-tower",
        WEBSITE_NAME_COLUMN: "Skyline Tower",
        "class_name": "SkylineTower",
        "platform": Platform.AWS,
        "location": "LIC",
        WEBSITE_RENT_TYPE: RentType.RENTAL,
    },
    {
        WEBSITE_URL_COLUMN: "https://streeteasy.com/building/altalic-29_22-northern-boulevard-long_island_city",
        WEBSITE_NAME_COLUMN: "AltaLIC",
        "class_name": "Alta",
        "platform": Platform.AWS,
        "location": "LIC",
        WEBSITE_RENT_TYPE: RentType.RENTAL,
    },
    {
        WEBSITE_URL_COLUMN: "https://streeteasy.com/building/watermark-lic",
        WEBSITE_NAME_COLUMN: "Watermark",
        "class_name": "Watermark",
        "platform": Platform.AWS,
        "location": "LIC",
        WEBSITE_RENT_TYPE: RentType.RENTAL,
    },
    {
        WEBSITE_URL_COLUMN: "https://streeteasy.com/building/qlic-41_42-24-street-long_island_city",
        WEBSITE_NAME_COLUMN: "QLIC",
        "class_name": "QLIC",
        "platform": Platform.AWS,
        "location": "LIC",
        WEBSITE_RENT_TYPE: RentType.RENTAL,
    },
    {
        WEBSITE_URL_COLUMN: "https://streeteasy.com/building/luna-lic",
        WEBSITE_NAME_COLUMN: "Luna",
        "class_name": "Luna",
        "platform": Platform.AWS,
        "location": "LIC",
        WEBSITE_RENT_TYPE: RentType.RENTAL,
    },
    {
        WEBSITE_URL_COLUMN: "https://streeteasy.com/building/one-lic",
        WEBSITE_NAME_COLUMN: "One LIC",
        "class_name": "OneLIC",
        "platform": Platform.AWS,
        "location": "LIC",
        WEBSITE_RENT_TYPE: RentType.RENTAL,
    },
    {
        WEBSITE_URL_COLUMN: "https://streeteasy.com/building/star-tower-lic",
        WEBSITE_NAME_COLUMN: "Star Tower",
        "class_name": "StarTower",
        "platform": Platform.AWS,
        "location": "LIC",
        WEBSITE_RENT_TYPE: RentType.RENTAL,
    },
    {
        WEBSITE_URL_COLUMN: "https://streeteasy.com/building/hero-condominium",
        WEBSITE_NAME_COLUMN: "Hero",
        "class_name": "Hero",
        "platform": Platform.AWS,
        "location": "LIC",
        WEBSITE_RENT_TYPE: RentType.RENTAL,
    },
    {
        WEBSITE_URL_COLUMN: "https://streeteasy.com/building/galerie-condominium",
        WEBSITE_NAME_COLUMN: "Galerie",
        "class_name": "Galerie",
        "platform": Platform.AWS,
        "location": "LIC",
        WEBSITE_RENT_TYPE: RentType.RENTAL,
    },
    {
        WEBSITE_URL_COLUMN: "https://streeteasy.com/building/22_22-jackson-avenue-long_island_city",
        WEBSITE_NAME_COLUMN: "22-22 Jackson Ave",
        "class_name": "JacksonAve",
        "platform": Platform.AWS,
        "location": "LIC",
        WEBSITE_RENT_TYPE: RentType.RENTAL,
    },
    {
        WEBSITE_URL_COLUMN: "https://streeteasy.com/building/aurora-condominium",
        WEBSITE_NAME_COLUMN: "Aurora",
        "class_name": "Aurora",
        "platform": Platform.AWS,
        "location": "LIC",
        WEBSITE_RENT_TYPE: RentType.RENTAL,
    },
    {
        WEBSITE_URL_COLUMN: "https://streeteasy.com/building/packard-square",
        WEBSITE_NAME_COLUMN: "Packard Square",
        "class_name": "PackardSquare",
        "platform": Platform.AWS,
        "location": "LIC",
        WEBSITE_RENT_TYPE: RentType.RENTAL,
    },
    {
        WEBSITE_URL_COLUMN: "https://streeteasy.com/building/packard-square-west",
        WEBSITE_NAME_COLUMN: "Packard Square West",
        "class_name": "PackardSquareWest",
        "platform": Platform.AWS,
        "location": "LIC",
        WEBSITE_RENT_TYPE: RentType.RENTAL,
    },
    {
        WEBSITE_URL_COLUMN: "https://streeteasy.com/building/the-pearson-court-square",
        WEBSITE_NAME_COLUMN: "Pearson CourtSquare",
        "class_name": "PearsonCourtSquare",
        "platform": Platform.AWS,
        "location": "LIC",
        WEBSITE_RENT_TYPE: RentType.RENTAL,
    },
    {
        WEBSITE_URL_COLUMN: "https://www.351marinjc.com/floorplans",
        WEBSITE_NAME_COLUMN: "351 Marin JC",
        "class_name": "351Marinjc",
        "platform": Platform.PYTHONANYWHERE,
        "location": "NJ",
        WEBSITE_RENT_TYPE: RentType.RENTAL,
    },
    {
        WEBSITE_URL_COLUMN: "https://www.grovepointe.com/floorplans",
        WEBSITE_NAME_COLUMN: "Grove Pointe",
        "class_name": "Gp",
        "platform": Platform.PYTHONANYWHERE,
        "location": "NJ",
        WEBSITE_RENT_TYPE: RentType.RENTAL,
    },
    {
        WEBSITE_URL_COLUMN: "https://www.235grand.com/floorplans",
        WEBSITE_NAME_COLUMN: "235 Grand Street",
        "class_name": "235GrandStreet",
        "platform": Platform.PYTHONANYWHERE,
        "location": "NJ",
        WEBSITE_RENT_TYPE: RentType.RENTAL,
    },
    {
        WEBSITE_URL_COLUMN: "https://www.485marin.com/floorplans",
        WEBSITE_NAME_COLUMN: "485 Marin",
        "class_name": "485Marin",
        "platform": Platform.PYTHONANYWHERE,
        "location": "NJ",
        WEBSITE_RENT_TYPE: RentType.RENTAL,
    },
    {
        WEBSITE_URL_COLUMN: "https://www.225grandstreet.com/floorplans",
        WEBSITE_NAME_COLUMN: "225 Grand Street",
        "class_name": "225GrandStreet",
        "platform": Platform.PYTHONANYWHERE,
        "location": "NJ",
        WEBSITE_RENT_TYPE: RentType.RENTAL,
    },
    {
        WEBSITE_URL_COLUMN: "https://www.18park.com/floorplans",
        WEBSITE_NAME_COLUMN: "18 Park",
        "class_name": "18Park",
        "platform": Platform.PYTHONANYWHERE,
        "location": "NJ",
        WEBSITE_RENT_TYPE: RentType.RENTAL,
    },
    {
        WEBSITE_URL_COLUMN: "https://www.journalsquared.com/availabilities",
        WEBSITE_NAME_COLUMN: "Journal Squared",
        "class_name": "Jsq",
        "platform": Platform.PYTHONANYWHERE,
        "location": "NJ",
        WEBSITE_RENT_TYPE: RentType.RENTAL,
    },
    {
        WEBSITE_URL_COLUMN: "https://www.ehomie.com/us/new-york/region-10001/apartment/e03s2",
        WEBSITE_NAME_COLUMN: "Ehomie Mid Manhattan",
        "class_name": "EhomieMidMan",
        "platform": Platform.PYTHONANYWHERE,
        "location": "Mid Manhattan",
        WEBSITE_RENT_TYPE: RentType.SUBLEASE,
    },
    {
        WEBSITE_URL_COLUMN: "https://www.ehomie.com/us/new-york/region-10002/apartment/e03s2",
        WEBSITE_NAME_COLUMN: "Ehomie Up Manhattan",
        "class_name": "EhomieUpMan",
        "platform": Platform.PYTHONANYWHERE,
        "location": "Up Manhattan",
        WEBSITE_RENT_TYPE: RentType.SUBLEASE,
    },
    {
        WEBSITE_URL_COLUMN: "https://www.ehomie.com/us/new-york/region-10003/apartment/e03s2",
        WEBSITE_NAME_COLUMN: "Ehomie NJ",
        "class_name": "EhomieNJ",
        "platform": Platform.PYTHONANYWHERE,
        "location": "NJ",
        WEBSITE_RENT_TYPE: RentType.SUBLEASE,
    },
    {
        WEBSITE_URL_COLUMN: "https://www.ehomie.com/us/new-york/region-10005/apartment/e03s2",
        WEBSITE_NAME_COLUMN: "Ehomie Brooklyn",
        "class_name": "EhomieBK",
        "platform": Platform.PYTHONANYWHERE,
        "location": "Brooklyn",
        WEBSITE_RENT_TYPE: RentType.SUBLEASE,
    },
    {
        WEBSITE_URL_COLUMN: "https://www.ehomie.com/us/new-york/region-10004/apartment/e03s2",
        WEBSITE_NAME_COLUMN: "Ehomie LIC Queen",
        "class_name": "EhomieLICQueen",
        "platform": Platform.PYTHONANYWHERE,
        "location": "LIC Queen",
        WEBSITE_RENT_TYPE: RentType.SUBLEASE,
    },
    {
        WEBSITE_URL_COLUMN: "https://www.ehomie.com/us/new-york/region-10006/apartment/e03s2",
        WEBSITE_NAME_COLUMN: "Ehomie Roosevelt",
        "class_name": "EhomieRoosevelt",
        "platform": Platform.PYTHONANYWHERE,
        "location": "Roosevelt",
        WEBSITE_RENT_TYPE: RentType.SUBLEASE,
    },
]


WEBSITES_DICT = {
    website["class_name"]: {**website, WEBSITE_PRIORITY_COLUMN: index}
    for index, website in enumerate(WEBSITES)
}

NOTIFICATION_EMAIL_SUBJECT = "【房源通知】"
ERROR_EMAIL_SUBJECT = "【房源抓取出错了】"
EMAIL_SENDER = "rent.spider.notification@gmail.com"
EMAIL_RECEIVERS_DEV = ["ppttzhu@gmail.com"]
EMAIL_RECEIVERS = ["atongmu0577@163.com", "panyuany1@163.com"]


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
    parser.add_argument("-a", "--auto", action="store_true", help="Automatic choose websites")
    parser.add_argument("-s", "--sublease", action="store_true", help="Sublease websites only")
    parser.add_argument("-r", "--remote", action="store_true", help="SSH to remote database")
    parser.add_argument("-u", "--update", action="store_true", help="Update website table")
    args = parser.parse_args()

    if os.environ.get("PYTHONANYWHERE_DOMAIN") is not None:
        PLATFORM = Platform.PYTHONANYWHERE
    elif args.remote:
        PLATFORM = Platform.AWS
    else:
        PLATFORM = Platform.DEV

    NEED_UPDATE_WEBSITE = args.update

    if args.include:
        WEBSITES_TARGETS = args.include
    elif args.exclude:
        WEBSITES_TARGETS = list(filter(lambda x: x not in args.exclude, WEBSITES_DICT.keys()))
    elif args.sublease:
        website_for_sublease = list(
            filter(lambda x: x[WEBSITE_RENT_TYPE] == RentType.SUBLEASE, WEBSITES)
        )
        WEBSITES_TARGETS = [w["class_name"] for w in website_for_sublease]
    elif args.auto and PLATFORM != Platform.DEV:
        website_for_platform = list(
            filter(
                lambda x: x["platform"] == PLATFORM and x[WEBSITE_RENT_TYPE] != RentType.SUBLEASE,
                WEBSITES,
            )
        )
        WEBSITES_TARGETS = [w["class_name"] for w in website_for_platform]
    else:
        WEBSITES_TARGETS = WEBSITES_DICT.keys()
except Exception:
    WEBSITES_TARGETS = WEBSITES_DICT.keys()
