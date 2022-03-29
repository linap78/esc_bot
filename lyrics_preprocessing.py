from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import pandas as pd
import re
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import os

sw = stopwords.words()

for file in os.listdir():
    if re.match(r"\d*\.txt", file):
        with open(file, "r", encoding="utf-8") as f:
            text = f.readlines()
            for i in text:
                if (
                    len(i.split()) <= 15
                    and len(i.split()) != 0
                    and re.search(
                        r"(Scroll|Written|Eurovision|A post|lyrics|Read more about|Prev|1 of 1|Next|juries and viewers|Speaking about the song|http[s]?|You can (check out|read|find)|#\w*?|Music & Lyrics:|Songtext|Photo credit:|themify_col grid=”2-1 first”|themify_col|What do you think about|YOU CAN FOLLOW|lyrics below|Will Nika Kocharov|Image:|Composed by:|Lyrics by:|Photo:|Music:|Additional reporting|VAL said the following|the song about|For starters,|The chorus goes:|tweet|@\w*?|Destiny (puts|allows)|Verse|Chorus|Bridge|Outro|Produced by:|English translation|Go_A said the following|final version|an official statement)",
                        i,
                    )
                    is None
                ):
                    with open("lyrics_output.txt", "a", encoding="utf-8") as t:
                        t.write(i)

with open("lyrics_output.txt", "r", encoding="utf-8") as f:
    txt = f.read()
    txt = sent_tokenize(txt)  # по предложениям
    txt = [w.lower() for w in txt]  # нижний регистр
    for s in range(len(txt)):
        txt[s] = re.sub(r"\n", " ", re.sub(r"[^-\w\s]", "", txt[s]))
        txt[s] = "".join([w + " " for w in txt[s].split() if w not in sw])
    txt_str = ""
    for s in txt:
        txt_str += s + " "
with open("lyrics_output.txt", "w", encoding="utf-8") as f:
    f.write(txt_str)

wordcloud = WordCloud(
    background_color="white",
    width=800,
    height=800,
).generate(txt_str)

plt.figure(figsize=(8, 8), facecolor=None)
plt.imshow(wordcloud)
plt.axis("off")
plt.title("Облако слов")
plt.show()
