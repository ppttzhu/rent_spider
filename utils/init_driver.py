import logging

import constants as c
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager


def init_driver():
    logging.info("Init webdriver...")
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    if c.IS_DEV or c.IS_REMOTE:
        return webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
    else:
        return webdriver.Chrome(
            ChromeDriverManager(version="90.0.4430.24").install(), options=chrome_options
        )
