import numpy as np
import matplotlib.pyplot as plt
import skfuzzy as fuzz
from sklearn.cluster import KMeans
from sklearn import metrics

# Define three cluster centers
centers = [[4, 2],
           [1, 7],
           [5, 6]]

# Define three cluster sigmas in x and y, respectively
sigmas = [[0.8, 0.3],
          [0.3, 0.5],
          [1.1, 0.7]]

# Generate test data
np.random.seed(42)  # Set seed for reproducibility
xpts = np.zeros(1)
ypts = np.zeros(1)
labels = np.zeros(1)
for i, ((xmu, ymu), (xsigma, ysigma)) in enumerate(zip(centers, sigmas)):
    xpts = np.hstack((xpts, np.random.standard_normal(200) * xsigma + xmu))
    ypts = np.hstack((ypts, np.random.standard_normal(200) * ysigma + ymu))
    labels = np.hstack((labels, np.ones(200) * i))
alldata = np.vstack((xpts, ypts))

# Fuzzy kmeans
cntr, u_orig, _, _, _, _, _ = fuzz.cluster.cmeans(
    alldata, 3, 2, error=0.005, maxiter=1000)
res1 = u_orig.argmax(axis=0)
fuzzy_kmeans_measures = list()
fuzzy_kmeans_measures.append(metrics.homogeneity_score(labels, res1))
fuzzy_kmeans_measures.append(metrics.completeness_score(labels, res1))
fuzzy_kmeans_measures.append(metrics.v_measure_score(labels, res1))
fuzzy_kmeans_measures.append(metrics.adjusted_rand_score(labels, res1))
fuzzy_kmeans_measures.append(metrics.silhouette_score(alldata.transpose(), res1, sample_size=1000))

# KMeans
km = KMeans(n_clusters=3, init='k-means++', max_iter=10000, tol=1e-5)
km.fit(alldata.transpose())
res2 = km.labels_
kmeans_measures = list()
kmeans_measures.append(metrics.homogeneity_score(labels, res2))
kmeans_measures.append(metrics.completeness_score(labels, res2))
kmeans_measures.append(metrics.v_measure_score(labels, res2))
kmeans_measures.append(metrics.adjusted_rand_score(labels, res2))
kmeans_measures.append(metrics.silhouette_score(alldata.transpose(), res2, sample_size=1000))

# Showing results
fig = plt.figure()
ax = fig.add_subplot(111)
ax.set_xticklabels(["Homogeneity", "Completeness",
                    "V-measure", "Adjusted rand index",
                    "Silhouette coefficient"])
ax.plot(kmeans_measures, "ro-", label="K-means")
ax.plot(fuzzy_kmeans_measures, "bx-", label="Fuzzy K-means")
ax.axis([0, 5, -1, 1])
plt.legend()
plt.show()
