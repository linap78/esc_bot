import requests
import time
import random
import re
from fake_useragent import UserAgent
from bs4 import BeautifulSoup

session = requests.session()

ua = UserAgent(verify_ssl=False)
headers = {"User-Agent": ua.random}

random.uniform(1, 3)

for _ in range(5):
    response = session.get("https://wiwibloggs.com/lyrics/", headers=headers)
    time.sleep(random.uniform(1.1, 5.2))

page = response.text
soup = BeautifulSoup(page, "html.parser")
text = soup.find("div", {"class": "content entry-content"})
links_attrs = text.find_all("a")

links = []
for i in range(len(links_attrs)):
    if re.search(r"\d{6}", links_attrs[i].attrs["href"]):
        links.append(links_attrs[i].attrs["href"])
    else:
        new_page = links_attrs[i].attrs["href"]

for _ in range(5):
    response = session.get(new_page, headers=headers)
    time.sleep(random.uniform(1.1, 5.2))

page = response.text
soup = BeautifulSoup(page, "html.parser")
text = soup.find("div", {"class": "content entry-content"})
links_attrs = text.find_all("a")
for i in range(len(links_attrs)):
    if re.search(r"\d{6}", links_attrs[i].attrs["href"]):
        links.append(links_attrs[i].attrs["href"])

for i in range(len(links)):
    for j in range(5):
        response = session.get(links[i], headers=headers)
        time.sleep(random.uniform(1.1, 5.2))

        page = response.text
        soup = BeautifulSoup(page, "html.parser")
        text = soup.find("div", {"class": "post-main"})
        text_attrs = text.find_all("p")

        lyrics = ""
        for l in text_attrs:
            lyrics += l.text
            lyrics += "\n"
            with open("{}.txt".format(str(i)), "w", encoding="utf-8") as f:
                f.write(lyrics)
