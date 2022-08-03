import argparse
import os

IS_REMOTE = None
IS_DEV = None
IS_PYTHONANYWHERE = os.environ.get("PYTHONANYWHERE_DOMAIN") is not None
WEBSITES_TARGETS = None

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

MINUTES_BETWEEN_FETCH = 5
TOTAL_DURATION_IN_MINUTES = 55
WEB_DRIVER_WAIT_SECOND = 10


WEBSITE_TABLE_NAME = "website"
WEBSITE_NAME_COLUMN = "website_name"
WEBSITE_URL_COLUMN = "url"
WEBSITE_PRIORITY_COLUMN = "priority"

ROOM_TABLE_NAME = "room"
ROOM_WEBSITE_NAME_COLUMN = "website_name"
ROOM_ROOM_NUMBER_COLUMN = "room_number"
ROOM_ROOM_TYPE_COLUMN = "room_type"
ROOM_MOVE_IN_DATE_COLUMN = "move_in_date"
ROOM_ROOM_PRICE_COLUMN = "room_price"
ROOM_FETCH_DATE_COLUMN = "fetch_date"
ROOM_TABLE_PRIMARY_KEY = [ROOM_WEBSITE_NAME_COLUMN, ROOM_ROOM_NUMBER_COLUMN]
ROOM_TABLE_COLUMNS = [
    ROOM_WEBSITE_NAME_COLUMN,
    ROOM_ROOM_TYPE_COLUMN,
    ROOM_ROOM_NUMBER_COLUMN,
    ROOM_MOVE_IN_DATE_COLUMN,
    ROOM_ROOM_PRICE_COLUMN,
]
ROOM_TABLE_COLUMNS_NAME = ["房源网站", "户型", "房号", "入住时间", "房价"]
ROOM_FETCH_DATE_COLUMN_NAME = "抓取时间"

WEBSITE_ROOM_VIEW_NAME = "v_website_room"
WEBSITE_ROOM_VIEW_ADDITIONAL_COLUMNS = [
    WEBSITE_URL_COLUMN,
    WEBSITE_PRIORITY_COLUMN,
]
WEBSITE_ROOM_VIEW_COLUMNS = ROOM_TABLE_COLUMNS + WEBSITE_ROOM_VIEW_ADDITIONAL_COLUMNS

WEBSITES = [
    {
        WEBSITE_URL_COLUMN: "https://streeteasy.com/building/qlic-41_42-24-street-long_island_city",
        WEBSITE_NAME_COLUMN: "Long Island City",
        "class_name": "QLIC",
    },
    {
        WEBSITE_URL_COLUMN: "https://streeteasy.com/building/skyline-tower",
        WEBSITE_NAME_COLUMN: "Skyline Tower",
        "class_name": "SkylineTower",
    },
    {
        WEBSITE_URL_COLUMN: "https://www.351marinjc.com/floorplans",
        WEBSITE_NAME_COLUMN: "351 Marin JC",
        "class_name": "351Marinjc",
    },
    {
        WEBSITE_URL_COLUMN: "https://www.grovepointe.com/floorplans",
        WEBSITE_NAME_COLUMN: "Grove Pointe",
        "class_name": "Gp",
    },
    {
        WEBSITE_URL_COLUMN: "https://www.235grand.com/floorplans",
        WEBSITE_NAME_COLUMN: "235 Grand Street",
        "class_name": "235GrandStreet",
    },
    {
        WEBSITE_URL_COLUMN: "https://www.485marin.com/floorplans",
        WEBSITE_NAME_COLUMN: "485 Marin",
        "class_name": "485Marin",
    },
    {
        WEBSITE_URL_COLUMN: "https://www.225grandstreet.com/floorplans",
        WEBSITE_NAME_COLUMN: "225 Grand Street",
        "class_name": "225GrandStreet",
    },
    {
        WEBSITE_URL_COLUMN: "https://www.18park.com/floorplans",
        WEBSITE_NAME_COLUMN: "18 Park",
        "class_name": "18Park",
    },
    {
        WEBSITE_URL_COLUMN: "https://www.journalsquared.com/availabilities",
        WEBSITE_NAME_COLUMN: "Journal Squared",
        "class_name": "Jsq",
    },
]

WEBSITES_DICT = {
    website["class_name"]: {**website, WEBSITE_PRIORITY_COLUMN: index}
    for index, website in enumerate(WEBSITES)
}

NOTIFICATION_EMAIL_SUBJECT = "【房源通知-测试】" if IS_DEV else "【房源通知】"
ERROR_EMAIL_SUBJECT = "【房源抓取出错了-测试】" if IS_DEV else "【房源抓取出错了】"
EMAIL_SENDER = "rent.spider.notification@gmail.com"
EMAIL_RECEIVERS_DEV = ["ppttzhu@gmail.com"]
EMAIL_RECEIVERS = EMAIL_RECEIVERS_DEV if IS_DEV else ["atongmu0577@163.com", "panyuany1@163.com"]

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
    parser.add_argument("-r", "--remote", action="store_true", help="Run in remote prod mode")
    parser.add_argument("-d", "--dev", action="store_true", help="Run in dev mode")
    parser.add_argument("-u", "--update", action="store_true", help="Update website table")
    args = parser.parse_args()
    IS_REMOTE = args.remote
    IS_DEV = args.dev
    if args.include:
        WEBSITES_TARGETS = args.include
    elif args.exclude:
        WEBSITES_TARGETS = list(filter(lambda x: x not in args.exclude, WEBSITES_DICT.keys()))
    else:
        WEBSITES_TARGETS = WEBSITES_DICT.keys()
except Exception:
    WEBSITES_TARGETS = WEBSITES_DICT.keys()
