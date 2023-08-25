import logging

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

import constants as c
from utils.user_agent import get_random_user_agent


def init_driver():
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
        import chromedriver_autoinstaller

        chromedriver_autoinstaller.install()
        return webdriver.Chrome(options=chrome_options)
    else:
        return webdriver.Chrome(
            ChromeDriverManager(version="90.0.4430.24").install(), options=chrome_options
        )
