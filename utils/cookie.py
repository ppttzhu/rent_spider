from time import sleep


def process_cookie_text(cookies):
    cookie_text = ""
    for cookie in cookies:
        if cookie["name"] in ["_actor", "_se_t", "se_lsa", "canadian", "_ses"]:
            cookie_text += f'{cookie["name"]}={cookie["value"]}; '
    return cookie_text


def check_blocked(html, cookies):
    if "Pardon Our Interruption" in html:
        print("We are blocked")
        return None
    else:
        cookies_text = process_cookie_text(cookies)
        return cookies_text


def get_selenium_cookie(driver, url="https://streeteasy.com"):
    driver.get(url)
    html = driver.page_source
    cookies = driver.get_cookies()
    return check_blocked(html, cookies)


def get_playwright_cookie(browser, url="https://streeteasy.com"):
    import constants as c
    from utils.user_agent import get_random_user_agent

    context = browser.new_context(user_agent=get_random_user_agent())
    page = context.new_page()
    page.goto(url, wait_until="domcontentloaded", timeout=c.WEB_DRIVER_TIMEOUT_SECOND * 1000)
    html = page.content()
    cookies = page.context.cookies()
    context.close()
    return check_blocked(html, cookies)


def refresh_and_store_cookies(selenium=True):
    MAX_RETRY = 3
    count = 0
    cookie_text = None
    while count < MAX_RETRY:
        if selenium:
            from utils.init_driver import init_driver

            driver = init_driver()
            cookie_text = get_selenium_cookie(driver)
            driver.quit()
        else:
            from playwright.sync_api import sync_playwright

            with sync_playwright() as play:
                browser = play.firefox.launch(headless=False)  # headless will be blocked
                cookie_text = get_playwright_cookie(browser)
                browser.close()
        if cookie_text:
            from database import Database

            print("Storing cookie in database: ", cookie_text)
            database = Database()
            database.save_cookie(cookie_text)
            database.quit()
            break
        else:
            count += 1
            sleep(30)
