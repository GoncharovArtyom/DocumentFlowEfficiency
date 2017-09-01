from sklearn.decomposition import TruncatedSVD
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import Normalizer
from sklearn.cluster import KMeans
from scipy import io
from time import time

import os
import matplotlib.pyplot as plt

# Settings
FROM_N_CLUSTERS = 3
TO_N_CLUSTERS = 100
N_COMPONENTS = 100
VERBOSE = False
N_INIT = 4
DATA_DIR = r"../Files/VectorizedData"

# Loading data
print("Loading data.")

X = io.mmread(os.path.join(DATA_DIR, "TfidfMatrix10000Features.mtx"))

print("%d samples." % X.shape[0])
print()

# LSA dimensionality reduction
if N_COMPONENTS:
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

# Do the actual clustering
print("Clustering sparse data with K-means")
errors = []
for k in range(FROM_N_CLUSTERS, TO_N_CLUSTERS + 1):
    km = KMeans(n_clusters=k, init='k-means++', max_iter=1000, n_init=N_INIT, tol=1e-5,
                verbose=VERBOSE)
    t0 = time()

    km.fit(X)
    errors.append(km.inertia_)

    print("Clustering for %d clusters is done in %0.3fs, error = %0.1f" % (k, (time() - t0),
                                                                           km.inertia_))

# Showing results
fig = plt.figure()
ax = fig.add_subplot(111)
ax.plot(list(range(FROM_N_CLUSTERS, TO_N_CLUSTERS + 1)), errors, "ro-",
        label="Optimization objective")
plt.legend()
plt.show()
