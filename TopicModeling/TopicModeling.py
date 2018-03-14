import os
import pickle
import time

from gensim import corpora, models, matutils
from scipy import io
from sklearn.feature_extraction.text import TfidfVectorizer

DATA_DIR = r"./Files/TopicModeling"
N_FEATURES = 1000
N_DOCUMENTS = 1000
N_TOPICS = 10
N_PASSES = 20

print("Loading data...")
# start_time = time.time()
#
# word_count_matrix_name = "CountWordMatrix_{n_docs}documents_{n_feats}features".format(
#     n_docs=N_DOCUMENTS, n_feats=N_FEATURES)
id_to_words_name = "FeatureNames_{n_docs}documents_{n_feats}features".format(
    n_docs=N_DOCUMENTS, n_feats=N_FEATURES)
#
# print("Loaded in {0:.2f}".format(time.time() - start_time))
# print("".center(25, "-"))
# print("Training...")
# start_time = time.time()
#
# data_sparse = io.mmread(os.path.join(DATA_DIR, word_count_matrix_name))
with open(os.path.join(DATA_DIR, id_to_words_name), "rb") as f:
    names = pickle.load(f)
#
# corpus = matutils.Sparse2Corpus(data_sparse, documents_columns=False)
# tfidf = models.TfidfModel(corpus, normalize=True)
# corpus_tfidf = tfidf[corpus]
# ldamodel = models.LdaModel(corpus_tfidf, num_topics=N_TOPICS, passes=N_PASSES,
#                            alpha=0.1)
# ldamodel.save(os.path.join(DATA_DIR, "models/ldamodel{}topics{}features{}documents".format(N_TOPICS,
#                                                                                            N_FEATURES,
#                                                                                            N_DOCUMENTS)))
#
# print("Trained in {0:.2f}".format(time.time() - start_time))
# print("".center(25, "-"))
# print("Topics' words:")
# print("".center(25, "*"))

ldamodel = models.LdaModel.load(os.path.join(DATA_DIR,"models/ldamodel{}topics{}features{}documents".format(N_TOPICS,
                                                                                            N_FEATURES,
                                                                                            N_DOCUMENTS)))

for topic in ldamodel.show_topics(formatted=False, num_words=10, num_topics=N_TOPICS):
    for word in topic[1]:
        print(names[int(word[0])], " ", word[1])
    print("".center(25, "*"))
