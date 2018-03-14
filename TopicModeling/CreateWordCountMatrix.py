import Stemmer
import logging
import math
import os
import pickle
import re
from time import time

from scipy import io
from sklearn.feature_extraction.text import CountVectorizer

from Analyzer import analyzer

# Settings
N_FEATURES = 10000
N_DOCUMENTS = 10000
SAVE_DIR = "../Files/TopicModeling"
DATA_DIR = "../Data"
STOP_WORDS_PATH = "../Files/VectorizedData/stop_words.txt"
FILE_TEMPLATE = "{name}_{n_docs}documents_{n_feats}features"

logging.basicConfig(level=logging.DEBUG, filename=os.path.join(SAVE_DIR, "logging.txt"),
                    filemode="w")

# Getting list of directories
file_pattern = re.compile(".*.txt$")
dir_list = os.listdir(DATA_DIR)
text_of_documents_list = []
document_id_list = []

# Creating string for each directory(id)
print("Loading data...")
t0 = time()
for dir_ in dir_list[:N_DOCUMENTS]:
    path = os.path.join(DATA_DIR, dir_)
    files = os.listdir(path)
    text = ""
    for file in files:
        if re.match(file_pattern, file):
            with open(os.path.join(path, file), "r") as f:
                try:
                    s = f.read()
                    text += s + " "
                except UnicodeDecodeError:
                    logging.error("encoding error in {} file".format(os.path.join(dir_, file)))
    if text != "":
        text_of_documents_list.append(text)
        document_id_list.append(dir_)
    else:
        logging.error("No txt files in {} directory".format(dir_))
t1 = time()
print("Finished in {}m {}s".format(math.floor((t1 - t0) / 60), math.floor((t1 - t0) % 60)))

print("-----------------------------------------------------------------------")
print("Extracting features from the dataset.")

stop_words = open(STOP_WORDS_PATH, "r").readlines()
stemmer = Stemmer.Stemmer("russian")
t0 = time()
vectorizer = CountVectorizer(max_df=0.5, max_features=N_FEATURES, min_df=10,
                             analyzer=lambda str_: analyzer(str_, stemmer, stop_words))
X = vectorizer.fit_transform(text_of_documents_list)

t1 = time()
print("Finished in {}m {}s".format(math.floor((t1 - t0) / 60), math.floor((t1 - t0) % 60)))
print("n_samples: %d, n_features: %d" % X.shape)
print()

names = vectorizer.get_feature_names()

# Save results
file_name = FILE_TEMPLATE.format(name="CountWordMatrix", n_docs=N_DOCUMENTS, n_feats=N_FEATURES)
io.mmwrite(os.path.join(SAVE_DIR, file_name), X)
file_name = FILE_TEMPLATE.format(name="DocumentIds", n_docs=N_DOCUMENTS, n_feats=N_FEATURES)
with open(os.path.join(SAVE_DIR, file_name), "wb") as f:
    pickle.dump(document_id_list, f)
file_name = FILE_TEMPLATE.format(name="FeatureNames", n_docs=N_DOCUMENTS, n_feats=N_FEATURES)
with open(os.path.join(SAVE_DIR, file_name), "wb") as f:
    pickle.dump(names, f)

