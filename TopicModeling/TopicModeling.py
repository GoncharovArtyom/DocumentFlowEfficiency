import os
import pickle

from gensim import corpora, models, matutils
from scipy import io
from sklearn.feature_extraction.text import TfidfVectorizer

DATA_DIR = r"./Files/TopicModeling"

# data_sparse = io.mmread(os.path.join(DATA_DIR, "CountWordMatrix10000Features.mtx"))
with open(os.path.join(DATA_DIR, "CountWordMatrix10000FeatureNames"), "rb") as f:
    names = pickle.load(f)

# corpus = matutils.Sparse2Corpus(data_sparse, documents_columns=False)
# tfidf = models.TfidfModel(corpus)
# corpus_tfidf = tfidf[corpus]
# ldamodel = models.LdaModel(corpus_tfidf)
# ldamodel.save(os.path.join(DATA_DIR,"models/ldamodel"))

ldamodel = models.LdaModel.load(os.path.join(DATA_DIR,"models/ldamodel"))

for topic in ldamodel.show_topics(formatted=False, num_words=5):
    for word in topic[1]:
        print(names[int(word[0])-1]," ", word[1])
    print("----------------")




