import getpass
import os

import requests
from bs4 import BeautifulSoup

import constants as c

web_url = "https://streeteasy.com/building/windermere-666-west-end-avenue-new_york/floorplans"
web_name = "morningside"  # for downloaded file name and folder name
download_path = f"/Users/{getpass.getuser()}/Downloads/{web_name}"  # for macos

# create folder if not exist
if not os.path.exists(download_path):
    os.makedirs(download_path)


def download_floorplan(room_id, url):
    r = requests.get(url, allow_redirects=True)
    file_format = url.split(".")[-1]
    download_full_path = f"{download_path}/{web_name}_{room_id}.{file_format}"
    if not os.path.exists(download_full_path):
        open(download_full_path, "wb").write(r.content)

def get_html_doc_with_scraperapi(url):
    print(f"Loading {url} with scraperapi...")
    payload = { 'api_key': c.CONFIG['scraperapi']['api_key'], 'url': url}
    response = requests.get('https://api.scraperapi.com/', params=payload)
    if "https://www.scraperapi.com/support" in response.text:
        raise Exception(f"scraperapi get html failed: {response.text}")
    return response.text


html_doc = get_html_doc_with_scraperapi(web_url)
soup = BeautifulSoup(html_doc, "html.parser")
div_elements = soup.find_all("div", {"class": "fp"})
links = {}
for element in div_elements:
    a_elements = element.find_all("a")
    room_id = a_elements[0].text
    links[room_id] = a_elements[1].get("href")
print(f"Removed duplicates and found {len(links)} links to download")
count = 0
failed_links = []
for room_id, url in links.items():
    count += 1
    print(f"Downloading {count}/{len(links)} from {url}", end="")
    try:
        download_floorplan(room_id, url)
        print(" - Done")
    except Exception as e:
        print(" - Failed" + str(e))
        failed_links.append(url)
print(f"Finished download to {download_path}")
print(f"{len(failed_links)} failed links: {failed_links}")
