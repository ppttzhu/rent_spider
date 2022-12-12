import logging

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

import constants as c


def init_driver():
    if c.PLATFORM == c.Platform.AWS:
        return None
    logging.info("Init webdriver...")
    chrome_options = webdriver.ChromeOptions()
    if c.PLATFORM != c.Platform.DEV:
        chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    if c.PLATFORM == c.Platform.DEV:
        # if version not available, have to download manually, unzip
        # https://chromedriver.storage.googleapis.com/106.0.5249.21/chromedriver_mac64_m1.zip
        # xattr -d com.apple.quarantine /Users/haley/Documents/git/chromedriver
        return webdriver.Chrome("/Users/haley/Documents/git/chromedriver", options=chrome_options)
    else:
        return webdriver.Chrome(
            ChromeDriverManager(version="90.0.4430.24").install(), options=chrome_options
        )
