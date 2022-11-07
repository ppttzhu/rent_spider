import logging

import constants as c
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager


def init_driver():
    logging.info("Init webdriver...")
    chrome_options = webdriver.ChromeOptions()
    if c.PLATFORM != c.Platform.DEV:
        chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    if c.PLATFORM != c.Platform.PYTHONANYWHERE:
        return webdriver.Chrome(
            ChromeDriverManager(version="106.0.5249.21").install(), options=chrome_options
        )
    else:
        return webdriver.Chrome(
            ChromeDriverManager(version="90.0.4430.24").install(), options=chrome_options
        )
