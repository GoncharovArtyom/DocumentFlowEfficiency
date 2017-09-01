from sklearn.datasets import fetch_20newsgroups
from sklearn.decomposition import TruncatedSVD
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import Normalizer
from sklearn import metrics

from sklearn.cluster import KMeans, MiniBatchKMeans

from time import time

import math

import matplotlib.pyplot as plt

import numpy as np

import warnings

import skfuzzy as fuzz

# Settings
N_FEATURES = 10000
N_INIT = 4
N_INIT_FUZZY = 1
N_COMPONENTS = 100
VERBOSE = 0

# Load some categories from the training set
# categories = [
#     'alt.atheism',
#     'talk.religion.misc',
#     'comp.graphics',
#     'sci.space',
# ]
categories = None
print("Loading 20 newsgroups dataset for categories:")
print(categories)

dataset = fetch_20newsgroups(subset='all', categories=categories, shuffle=True, random_state=42,
                             remove=('headers', 'footers', 'quotes'))

print("%d documents" % len(dataset.data))
print("%d categories" % len(dataset.target_names))
print()

labels = dataset.target
true_k = np.unique(labels).shape[0]

print("Extracting features from the training dataset using a sparse vectorizer")
t0 = time()

vectorizer = TfidfVectorizer(max_df=0.5, max_features=N_FEATURES, min_df=2, stop_words='english')
X = vectorizer.fit_transform(dataset.data)

print("done in %fs" % (time() - t0))
print("n_samples: %d, n_features: %d" % X.shape)
print()

# Comparison
# KMeans
print("-----------------------------------")
print("Clustering sparse data with K-means")

kmeans_measures = []
km = KMeans(n_clusters=true_k, init='k-means++', max_iter=10000, n_init=N_INIT, tol=1e-5,
            verbose=VERBOSE)
t0 = time()
km.fit(X)

print("done in %0.3fs" % (time() - t0))
print()

kmeans_measures.append(metrics.homogeneity_score(labels, km.labels_))
kmeans_measures.append(metrics.completeness_score(labels, km.labels_))
kmeans_measures.append(metrics.v_measure_score(labels, km.labels_))
kmeans_measures.append(metrics.adjusted_rand_score(labels, km.labels_))
kmeans_measures.append(metrics.silhouette_score(X, km.labels_, sample_size=1000))

print("Homogeneity: %0.3f" % kmeans_measures[0])
print("Completeness: %0.3f" % kmeans_measures[1])
print("V-measure: %0.3f" % kmeans_measures[2])
print("Adjusted Rand-Index: %.3f" % kmeans_measures[3])
print("Silhouette Coefficient: %0.3f" % kmeans_measures[4])

# MiniBatch K-means
print("-----------------------------------")
print("Clustering sparse data with K-means")

mini_batch_kmeans_measures = []
km = MiniBatchKMeans(n_clusters=true_k, init='k-means++', max_iter=10000, n_init=N_INIT,
                     tol=1e-5, verbose=VERBOSE)
t0 = time()
with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    km.fit(X)

print("done in %0.3fs" % (time() - t0))
print()

mini_batch_kmeans_measures.append(metrics.homogeneity_score(labels, km.labels_))
mini_batch_kmeans_measures.append(metrics.completeness_score(labels, km.labels_))
mini_batch_kmeans_measures.append(metrics.v_measure_score(labels, km.labels_))
mini_batch_kmeans_measures.append(metrics.adjusted_rand_score(labels, km.labels_))
mini_batch_kmeans_measures.append(metrics.silhouette_score(X, km.labels_, sample_size=1000))

print("Homogeneity: %0.3f" % mini_batch_kmeans_measures[0])
print("Completeness: %0.3f" % mini_batch_kmeans_measures[1])
print("V-measure: %0.3f" % mini_batch_kmeans_measures[2])
print("Adjusted Rand-Index: %.3f" % mini_batch_kmeans_measures[3])
print("Silhouette Coefficient: %0.3f" % mini_batch_kmeans_measures[4])

# Fuzzy kmeans
print("-----------------------------------")
print("Clustering dense data with Fuzzy k-means")

fuzzy_kmeans_measures = []
data = X.todense().transpose()
res_labels = []
t0 = time()
max_fpc = -math.inf
for i in range(N_INIT_FUZZY):
    cntr, res, _, _, _, p, fpc = fuzz.cluster.cmeans(data, true_k, 2, error=1e-5, maxiter=10000)
    if fpc > max_fpc:
        res_labels = res.argmax(axis=0)
        max_fpc = fpc
    print("%d steps" % p)

print("done in %0.3fs" % (time() - t0))
print()

fuzzy_kmeans_measures.append(metrics.homogeneity_score(labels, res_labels))
fuzzy_kmeans_measures.append(metrics.completeness_score(labels, res_labels))
fuzzy_kmeans_measures.append(metrics.v_measure_score(labels, res_labels))
fuzzy_kmeans_measures.append(metrics.adjusted_rand_score(labels, res_labels))
fuzzy_kmeans_measures.append(metrics.silhouette_score(X, res_labels, sample_size=1000))

print("Homogeneity: %0.3f" % fuzzy_kmeans_measures[0])
print("Completeness: %0.3f" % fuzzy_kmeans_measures[1])
print("V-measure: %0.3f" % fuzzy_kmeans_measures[2])
print("Adjusted Rand-Index: %.3f" % fuzzy_kmeans_measures[3])
print("Silhouette Coefficient: %0.3f" % fuzzy_kmeans_measures[4])

# LSA
print()
print("---------------------------------------------")
print("Performing dimensionality reduction using LSA")

t0 = time()
svd = TruncatedSVD(N_COMPONENTS)
normalizer = Normalizer(copy=False)
lsa = make_pipeline(svd, normalizer)
X = lsa.fit_transform(X)

print("done in %fs" % (time() - t0))
explained_variance = svd.explained_variance_ratio_.sum()
print("Explained variance of the SVD step: {}%".format(
    int(explained_variance * 100)))
print()

# KMeans lsa
print("-----------------------------------")
print("Clustering redundant data with K-means")

kmeans_measures_lsa = []
km = KMeans(n_clusters=true_k, init='k-means++', max_iter=10000, n_init=N_INIT, tol=1e-5,
            verbose=VERBOSE)
t0 = time()
km.fit(X)

print("done in %0.3fs" % (time() - t0))
print()

kmeans_measures_lsa.append(metrics.homogeneity_score(labels, km.labels_))
kmeans_measures_lsa.append(metrics.completeness_score(labels, km.labels_))
kmeans_measures_lsa.append(metrics.v_measure_score(labels, km.labels_))
kmeans_measures_lsa.append(metrics.adjusted_rand_score(labels, km.labels_))
kmeans_measures_lsa.append(metrics.silhouette_score(X, km.labels_, sample_size=1000))

print("Homogeneity: %0.3f" % kmeans_measures_lsa[0])
print("Completeness: %0.3f" % kmeans_measures_lsa[1])
print("V-measure: %0.3f" % kmeans_measures_lsa[2])
print("Adjusted Rand-Index: %.3f" % kmeans_measures_lsa[3])
print("Silhouette Coefficient: %0.3f" % kmeans_measures_lsa[4])

print("-----------------------------------")
print("Clustering redundant data with Fuzzy k-means")

fuzzy_kmeans_measures_lsa = []
data = X.transpose()
t0 = time()
max_fpc = -math.inf
for j in range(N_INIT_FUZZY):
    _, res, _, _, _, p, fpc = fuzz.cluster.cmeans(data, true_k, 2, error=1e-5, maxiter=10000)
    if fpc > max_fpc:
        res_labels = res.argmax(axis=0)
        max_fpc = fpc
    print("%d steps" % p)
print("done in %0.3fs" % (time() - t0))
print()

fuzzy_kmeans_measures_lsa.append(metrics.homogeneity_score(labels, res_labels))
fuzzy_kmeans_measures_lsa.append(metrics.completeness_score(labels, res_labels))
fuzzy_kmeans_measures_lsa.append(metrics.v_measure_score(labels, res_labels))
fuzzy_kmeans_measures_lsa.append(metrics.adjusted_rand_score(labels, res_labels))
fuzzy_kmeans_measures_lsa.append(metrics.silhouette_score(X, res_labels, sample_size=1000))

print("Homogeneity: %0.3f" % fuzzy_kmeans_measures_lsa[0])
print("Completeness: %0.3f" % fuzzy_kmeans_measures_lsa[1])
print("V-measure: %0.3f" % fuzzy_kmeans_measures_lsa[2])
print("Adjusted Rand-Index: %.3f" % fuzzy_kmeans_measures_lsa[3])
print("Silhouette Coefficient: %0.3f" % fuzzy_kmeans_measures_lsa[4])

# Showing results
fig = plt.figure()
ax = fig.add_subplot(111)
ax.set_xticklabels(["Homogeneity", "Completeness",
                    "V-measure", "Adjusted rand index",
                    "Silhouette coefficient"])
ax.plot(kmeans_measures, "ro-", label="K-means")
ax.plot(mini_batch_kmeans_measures, "go-", label="Mini-batch K-means")
ax.plot(fuzzy_kmeans_measures, "bo-", label="Fuzzy K-means")
ax.plot(kmeans_measures_lsa, "co-", label="K-means LSA")
ax.plot(fuzzy_kmeans_measures_lsa, "mo-", label="Fuzzy K-means LSA")
ax.axis([0, 5, -1, 1])
plt.legend()
plt.show()
