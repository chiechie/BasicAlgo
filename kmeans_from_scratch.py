import pandas as pd
 import numpy as np
from scipy.spatial.distance import cdist 
from sklearn.datasets import load_digits
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt


K = 10
N_iter = 10
cluster = {}
data = load_digits().data
data = PCA(2).fit_transform(data)

## 随机生成出初始中心点

centorid_id = np.random.permutation(data.shape[0])[:K]
centroid = {k: data[centorid_id[k], :] for k in range(K)}

for n_iter in range(N_iter):
    ## 重新分配cluster：将每个样本归类到离它最近的中心点中，结果存储为dict
    cluster = {}
    for i, x in enumerate(data):
        values = [np.sum((x - centroid[k])**2) for k in range(K)]
        cluster_id = values.index(min(values))
        cluster.setdefault(cluster_id, [i]).append(i)
    ## 重新生成中心点
    for k in range(K):
        centroid[k] = data[cluster[k], :].mean(axis=0) 
        
#Visualize the results
for k in range(K):
    plt.scatter(data[cluster[k], 0] ,  data[cluster[k], 1] , label = k)
plt.legend()
plt.show()