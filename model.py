import gensim
import logging
import urllib.request
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt

import warnings

warnings.filterwarnings("ignore")

f = "lyrics_output.txt"
data = gensim.models.word2vec.LineSentence(f)
model = gensim.models.Word2Vec(data, vector_size=300, window=5, min_count=5, epochs=50)
model.wv.save_word2vec_format("model.bin.gz", binary=True)

print(model.wv.most_similar("love", topn=10))

words = ["oh", "hey", "yay", "ah", "yeah"]
print(model.wv.doesnt_match(words))
print(model.wv.most_similar("yay", topn=10))


m = "model.bin.gz"
model = gensim.models.KeyedVectors.load_word2vec_format(m, binary=True)
X = model[words]

pca = PCA(n_components=2)
coords = pca.fit_transform(X)

plt.scatter(coords[:, 0], coords[:, 1], color="red")
plt.title("Words")

for i, word in enumerate(words):
    plt.annotate(word, xy=(coords[i, 0], coords[i, 1]))
plt.show()
