"""
reference : https://en.wikipedia.org/wiki/PageRank
"""
import numpy as np

def pr(adjacency_arr, N_iter = 20, d = 0.85):
    M = np.zeros(adjacency_arr.shape)
    for m in range(M.shape[0]):
        M[:, m] = adjacency_arr[:, m] / adjacency_arr[:, m].sum()

    e = np.ones(adjacency_arr.shape[0])*1.0 / adjacency_arr.shape[0]
    v0 = e.copy()
    for i in range(N_iter):
        vn = np.dot(M, v0)*d + e*(1-d)
        v0 = vn
    return vn


if __name__ == "__main__":
	adjacency_arr = np.array([[0, 0, 0, 0, 1],
	              [0.5, 0, 0, 0, 0],
	              [0.5, 0, 0, 0, 0],
	              [0, 1, 0.5, 0, 0],
	              [0, 0, 0.5, 1, 0]])
	print("ground truth\n", [[0.25419178],
	       [0.13803151],
	       [0.13803151],
	       [0.20599017],
	       [0.26375504]])
	vn = pr(adjacency_arr, N_iter = 100, d = 0.85)
	print("result\n", vn)