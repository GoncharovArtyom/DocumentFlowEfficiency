import artm
import os
import pandas as pd
import pickle
import numpy as np
import matplotlib.pyplot as plt

from CreateUnitsTree import Organization
from sklearn.cluster import KMeans

DATA_DIR = r"../Files"
ORGANIZATION_FILE = os.path.join(DATA_DIR, "organization.json")

N_DOCUMENTS = 10000
BASE_DIR = "../Files/TopicModeling/{}_documents".format(N_DOCUMENTS)
SAVE_DIR = os.path.join(BASE_DIR, "models/artm")
THETA_FILE = os.path.join(BASE_DIR, "theta.pkl")
PHI_FILE = os.path.join(BASE_DIR, "phi.pkl")
ID_TO_ROW_FILE_NAME = os.path.join("../Files/DataPreprocessing",
                                   "{name}_{n_docs}documents_{n_feats}features".format(
                                        name="id_to_row",
                                        n_docs=N_DOCUMENTS,
                                        n_feats=1000))

model_artm = artm.load_artm_model(SAVE_DIR)

organization = Organization.Organization.LoadFromJson(ORGANIZATION_FILE)
employees = list(organization.GetAllEmployees())

theta = pd.read_pickle(THETA_FILE).values
with open(ID_TO_ROW_FILE_NAME, "rb") as id_to_row_file:
    id_to_row = pickle.load(id_to_row_file)

employee_to_vectors = {}
for employee in employees:
    employee_to_vectors[employee] = []
    for document_id in employee.Documents:
        if document_id in id_to_row:
            employee_to_vectors[employee].append(theta[:, id_to_row[document_id]])

employee_to_vectors = [(key,np.mean(np.array(value), axis=0)) for key, value in
                       employee_to_vectors.items()\
        if value]
X = np.array([vector for _, vector in employee_to_vectors])

scores = []
for n_clusters in range(3, 11):
    kmeans = KMeans(n_clusters=n_clusters)
    kmeans.fit(X)
    scores.append(np.abs(kmeans.score(X)))

plt.plot(range(3, 11), scores, linewidth=2)
plt.xlabel("n_clusters")
plt.ylabel("objective")
plt.show()
