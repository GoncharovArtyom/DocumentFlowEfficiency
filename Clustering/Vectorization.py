import os
import Stemmer
import pickle
import logging
import math
import re

from Analyzer import analyzer
from sklearn.feature_extraction.text import TfidfVectorizer
from scipy import io
from time import time

# Settings
N_FEATURES = 10000
SAVE_DIR = "../Files/VectorizedData"
DATA_DIR = "../Data"

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
for dir_ in dir_list:
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
stemmer = Stemmer.Stemmer("russian")
t0 = time()
vectorizer = TfidfVectorizer(max_df=0.5, max_features=N_FEATURES, min_df=2,
                             analyzer=lambda str_: analyzer(str_, stemmer))
X = vectorizer.fit_transform(text_of_documents_list)

t1 = time()
print("Finished in {}m {}s".format(math.floor((t1 - t0) / 60), math.floor((t1 - t0) % 60)))
print("n_samples: %d, n_features: %d" % X.shape)
print()

# Save results
io.mmwrite(os.path.join(SAVE_DIR, "TfidfMatrix{}Features".format(N_FEATURES)), X)
with open(os.path.join(SAVE_DIR, "DocumentIds"), "wb") as f:
    pickle.dump(document_id_list, f)
