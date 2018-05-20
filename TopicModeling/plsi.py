import artm
import os
import pickle
import time
import shutil
import matplotlib.pyplot as plt

from scipy import io
from sklearn.feature_extraction.text import TfidfVectorizer

N_DOCUMENTS = 1000
N_TOPICS = 10
N_PASSES = 10

DATA_DIR = "../Files/DataPreprocessing/{}_documents".format(N_DOCUMENTS)
BASE_DIR = "../Files/TopicModeling/{}_documents".format(N_DOCUMENTS)
SAVE_DIR = os.path.join(BASE_DIR, "models/plsi")

BATCHES_DIR = os.path.join(BASE_DIR, "batches")
DICTIONARY_FILE = os.path.join(BASE_DIR, "dictionary.dict")
COOC_FILE = os.path.join(BASE_DIR, "cooc_tf")
VOCAB_FILE = os.path.join(DATA_DIR, "vocab")

start = time.time()
bv = artm.BatchVectorizer(data_path=BATCHES_DIR,
                          data_format="batches")
dictionary = artm.Dictionary()
dictionary.load(DICTIONARY_FILE)

cooc_dict = artm.Dictionary()
cooc_dict.gather(
    data_path=BATCHES_DIR,
    cooc_file_path=COOC_FILE,
    vocab_file_path=VOCAB_FILE,
    symmetric_cooc_values=True)

coherence_score = artm.TopTokensScore(
                            name='TopTokensCoherenceScore',
                            dictionary=cooc_dict,
                            num_tokens=10)

model_artm = artm.ARTM(num_topics=N_TOPICS)

model_artm.scores.add(artm.TopTokensScore(name="top_words", num_tokens=10))
model_artm.scores.add(coherence_score)
model_artm.scores.add(artm.PerplexityScore(name='perplexity_score',
                                      dictionary=bv.dictionary))
model_artm.scores.add(artm.SparsityPhiScore(name='sparsity_phi_score'))
model_artm.scores.add(artm.SparsityThetaScore(name='sparsity_theta_score'))

model_artm.initialize(dictionary=dictionary)
print("Initializing time: {}".format(time.time() - start))

start = time.time()
model_artm.fit_offline(bv, num_collection_passes=N_PASSES)
print("Training time: {}".format(time.time() - start))

if os.path.isdir(SAVE_DIR):
    shutil.rmtree(SAVE_DIR)
model_artm.dump_artm_model(SAVE_DIR)
# model_artm = artm.load_artm_model(SAVE_DIR)

for topic_name in model_artm.topic_names:
    print("".center(25, "*"))
    score_tracker = model_artm.score_tracker["top_words"]
    for word, prob in zip(score_tracker.last_tokens[topic_name], score_tracker.last_weights[
        topic_name]):
        print("{}: {:.5f}".format(word, prob))

print("".center(25, "*"))
print("sparsity phi score:", model_artm.score_tracker[
    'sparsity_phi_score'].last_value)
print("sparsity theta score:", model_artm.score_tracker[
    'sparsity_theta_score'].last_value)
print("perplexity: ", model_artm.score_tracker['perplexity_score'].last_value)
print("coherence: ", model_artm.score_tracker['TopTokensCoherenceScore'].average_coherence)

plt.plot(model_artm.score_tracker['perplexity_score'].value)
plt.show()