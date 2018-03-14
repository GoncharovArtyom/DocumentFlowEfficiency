import artm
import os
import pickle
import time
import matplotlib.pyplot as plt

from scipy import io
from sklearn.feature_extraction.text import TfidfVectorizer

DATA_DIR = r"../Files/TopicModeling"
N_FEATURES = 1000
N_DOCUMENTS = 1000
N_TOPICS = 10
N_PASSES = 20

print("Loading data...")
start_time = time.time()

word_count_matrix_name = "CountWordMatrix_{n_docs}documents_{n_feats}features".format(
    n_docs=N_DOCUMENTS, n_feats=N_FEATURES)
id_to_words_name = "FeatureNames_{n_docs}documents_{n_feats}features".format(
    n_docs=N_DOCUMENTS, n_feats=N_FEATURES)

data = io.mmread(os.path.join(DATA_DIR, word_count_matrix_name)).todense().T
with open(os.path.join(DATA_DIR, id_to_words_name), "rb") as f:
    names = pickle.load(f)

id_to_words = {ind:word for ind, word in enumerate(names)}

print("Loaded in {0:.2f}".format(time.time() - start_time))
print("".center(25, "-"))
print("Training...")
start_time = time.time()

bv = artm.BatchVectorizer(data_format='bow_n_wd',
                          n_wd=data,
                          vocabulary=id_to_words)

model_artm = artm.ARTM(num_topics=N_TOPICS, topic_names=["sbj{}".format(i) for i in range(
    N_TOPICS)], dictionary=bv.dictionary)
model_artm.scores.add(artm.TopTokensScore(name="top_words", num_tokens=10))
model_artm.scores.add(artm.PerplexityScore(name='perplexity_score',
                                      dictionary=bv.dictionary))
model_artm.scores.add(artm.SparsityPhiScore(name='sparsity_phi_score'))
model_artm.scores.add(artm.SparsityThetaScore(name='sparsity_theta_score'))

model_artm.regularizers.add(artm.SmoothSparsePhiRegularizer(tau=-5))

model_artm.fit_offline(bv, num_collection_passes=N_PASSES)

for topic_name in model_artm.topic_names:
    print("".center(25, "*"))
    for word in model_artm.score_tracker["top_words"].last_tokens[topic_name]:
        print(word)

print("".center(25, "*"))
print("sparsity phi dcore:", model_artm.score_tracker['sparsity_phi_score'].last_value)
print("sparsity theta score:", model_artm.score_tracker['sparsity_theta_score'].last_value)

plt.plot(model_artm.score_tracker['perplexity_score'].value)
plt.show()

