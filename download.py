import os
import re

import requests
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

from fetch.fetch1QPS import Fetch1QPS

web_url = "https://streeteasy.com/building/eagle-lofts/floorplans"
web_name = "Eagle Lofts"  # for downloaded file name and folder name
download_path = f"/Users/haley/Desktop/{web_name}"

# create folder if not exist
if not os.path.exists(download_path):
    os.makedirs(download_path)


def download_floorplan(room_id, url):
    r = requests.get(url, allow_redirects=True)
    file_format = url.split(".")[-1]
    download_full_path = f"{download_path}/{web_name}_{room_id}.{file_format}"
    if not os.path.exists(download_full_path):
        open(download_full_path, "wb").write(r.content)


with sync_playwright() as play:
    browser = play.firefox.launch(headless=False)
    fetcher = Fetch1QPS(None, browser)
    html_doc = fetcher.get_html_doc(web_url)
    soup = BeautifulSoup(html_doc, "html.parser")
    a_elements = soup.find_all("a", text=re.compile("^click to view .* floorplan$"))
    links = {}
    for element in a_elements:
        room_id = fetcher.get_substring_by_regex(
            element.get_text(), r"^click to view (.+?) floorplan$"
        ).replace("#", "")
        links[room_id] = element.get("href")
    print(f"Removed duplicates and found {len(links)} links to download")
    count = 0
    for room_id, url in links.items():
        count += 1
        print(f"Downloading {count}/{len(links)} from {url}")
        download_floorplan(room_id, url)
