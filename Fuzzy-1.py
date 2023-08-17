
import random
import numpy as np
from sklearn.datasets import make_blobs
import cMean_Clustering
import gustafson_Clustering
import image_fuzzy

path = "5.jpg"
path2 = "4.jpg"
number_of_clusters = 5
samples = 200
std = 1.5
min_err = 0.001 
max_iter = 100 
m = 2

data, labels_true = make_blobs(n_samples=samples, centers=number_of_clusters,
                  cluster_std=std, random_state=random.randint(0, 200))

cMean_Clustering.cMeans(data, labels_true,number_of_clusters,m,min_err,max_iter)
gustafson_Clustering.gustafson(data, labels_true,number_of_clusters,m,min_err,max_iter)

cMean_Clustering.imageCMeans(path,np.ones((300,300)),number_of_clusters)
gustafson_Clustering.imagegustafson(path,np.ones((300,300)),number_of_clusters)

image_fuzzy.imageFuzzy(path2)

