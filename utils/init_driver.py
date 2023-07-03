import logging

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

import constants as c
from utils.user_agent import get_random_user_agent


def init_driver():
    if c.PLATFORM == c.Platform.AWS:
        return None
    logging.info("Init webdriver...")

    chrome_options = webdriver.ChromeOptions()
    if c.PLATFORM != c.Platform.DEV:
        chrome_options.add_argument("--headless")
    chrome_options.add_argument(f"user-agent={get_random_user_agent()}")
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    if c.PLATFORM == c.Platform.DEV:
        # if version not available, have to download manually, unzip
        # https://chromedriver.storage.googleapis.com/110.0.5481.30/chromedriver_mac_arm64.zip
        # If not trusted, run this command in terminal
        # xattr -d com.apple.quarantine /Users/haley/Documents/git/chromedriver
        return webdriver.Chrome("/Users/haley/Documents/git/chromedriver", options=chrome_options)
    else:
        return webdriver.Chrome(
            ChromeDriverManager(version="90.0.4430.24").install(), options=chrome_options
        )
