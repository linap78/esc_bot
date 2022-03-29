from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from pymystem3 import Mystem
import pandas as pd
import re
import matplotlib.pyplot as plt
from wordcloud import WordCloud

m = Mystem()

sw = stopwords.words("russian")

df = pd.read_csv("eu_news.csv", sep="\t")
text = ""
for i in range(7):
    text += df["news_texts"][i]

text = sent_tokenize(text)  # по предложениям
text = [w.lower() for w in text]  # нижний регистр
for s in range(len(text)):
    text[s] = re.sub(r"\n", " ", re.sub(r"[^-\w\s]", "", text[s]))
text_str = ""
for s in text:
    text_str += s + " "
lemmas = str([w + " " for w in "".join(m.lemmatize(text_str)).split() if w not in sw])

wordcloud = WordCloud(
    background_color="white",
    width=800,
    height=800,
).generate(lemmas)

plt.figure(figsize=(8, 8), facecolor=None)
plt.imshow(wordcloud)
plt.axis("off")
plt.title("Облако слов")
plt.show()
