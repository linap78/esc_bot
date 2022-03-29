import requests
import time
import random
import re
from fake_useragent import UserAgent
from bs4 import BeautifulSoup

import pandas as pd

session = requests.session()

ua = UserAgent(verify_ssl=False)
headers = {"User-Agent": ua.random}

random.uniform(1, 3)

for _ in range(5):
    response = session.get(
        "https://ria.ru/event_Konkurs_pesni_Evrovidenie/", headers=headers
    )
    time.sleep(random.uniform(1.1, 5.2))

page = response.text
soup = BeautifulSoup(page, "html.parser")
text = soup.find_all("a", {"class": "list-item__title color-font-hover-only"})

names = []
links = []
texts = []

for i in range(7):
    names.append(text[i].text)
    links.append(text[i].attrs["href"])

for i in links:
    txt = ""
    for j in range(5):
        response = session.get(i, headers=headers)
        time.sleep(random.uniform(1.1, 5.2))

        page = response.text
        soup = BeautifulSoup(page, "html.parser")
        text_list = soup.find_all("div", {"class": "article__text"})
    for t in text_list:
        txt += t.text + " "
    texts.append(txt)

data = {"news_name": names[:7], "age": links[:7], "news_texts": texts}

df = pd.DataFrame(data)
df.to_csv("eu_news.csv", index=None, sep="\t")
