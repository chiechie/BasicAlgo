import matplotlib
matplotlib.use('TkAgg')

import  matplotlib.pyplot as plt
matplotlib.rcParams['figure.figsize'] = (10.0, 8.0)

import numpy as np
import sklearn
import sklearn.datasets
import sklearn.linear_model


def train(X, Y, hidden_units, eps = 1e-15, n_epochs = 20000, learning_rate = 0.01):
	W1 = np.random.randn(hidden_units, m_features + 1) / np.sqrt(hidden_units)
	W2 = np.random.randn(2, hidden_units + 1 ) / np.sqrt(hidden_units)

	for epoch in range(n_epochs):
		[H, H_full, logits, probs] = foward(X, W1, W2)
		loss = - Y * np.log(probs) - (1 - Y) * np.log(1 - probs)
		[delta_W2, delta_W1] = backward(probs, Y, H_full, W2, H)
		W1 -= delta_W1 * learning_rate
		W2 -= delta_W2 * learning_rate
		if epoch % 5000 == 0:
			print("epoch={}, total_loss={}".format(epoch, sum(loss)))
	return W1, W2, probs


def foward(X, W1, W2):
	X_full = np.concatenate((X, np.ones((X.shape[0], 1))), axis = 1)
	H = np.tanh(X_full.dot(W1.T))
	H_full = np.concatenate((H, np.ones((X.shape[0], 1))), axis = 1)
	logits = H_full.dot(W2.T)
	probs = 1.0 / (1 + np.exp( - logits))
	probs[probs < 1e-15 ] = 1e-15
	probs[probs > 1 - 1e-15] =1 - 1e-15
	return H, H_full, logits, probs


def backward(probs, Y, H_full, W2, H):
	delta_logits = probs - Y 	

	delta_W2 =  np.dot(delta_logits.T, H_full)

	delta_H = np.dot(delta_logits, W2)

	delta_a = delta_H[:, :-1] * ( 1 - H**2)

	delta_W1 = np.dot(delta_a.T,  X_full)
	return delta_W2, delta_W1


if __name__ == "__main__":
	np.random.seed(0)
	X, Y = sklearn.datasets.make_moons(200, noise=0.20)
	Y = Y.reshape(-1, 1)
	n_samples, m_features = X.shape

	# 0. 设置网络结构
	hidden_units = 5
	output_units = 1

	# 1. 初始化权重向量
	W1 = np.random.randn(hidden_units, m_features + 1) / np.sqrt(hidden_units)
	W2 = np.random.randn(1, hidden_units + 1 ) / np.sqrt(hidden_units)
	assert(W1.shape == (5, 3))
	assert(W2.shape == (1, 6))


	# 2. 开始训练
	## 2.1 向前传播
	X_full = np.concatenate((X, np.ones((n_samples, 1))), axis = 1)
	assert(X_full.shape == (200, 3))
	H = np.tanh(X_full.dot(W1.T))
	assert(H.shape == (200, 5))

	H_full = np.concatenate((H, np.ones((n_samples, 1))), axis = 1)
	assert(H_full.shape == (200, 6))

	logits = H_full.dot(W2.T)
	assert(logits.shape == (200, 1))

	probs = 1.0 / (1 + np.exp(logits))
	assert(probs.shape == (200, 1))

	loss = - Y * np.log(probs) - (1 - Y) * np.log(1 - probs)
	print(loss.shape)
	assert(loss.shape == (200, 1))

	## 2.2 向后传播
	# 交叉熵损失对于logits的梯度越过中间变量prob直接算出来, 即
	# df/dlogits =  probs - Y

	delta_logits = probs - Y 	
	assert(delta_logits.shape == (200, 1))

	delta_W2 =  np.dot(delta_logits.T, H_full)
	assert(delta_W2.shape == (1, 6))

	delta_H = np.dot(delta_logits, W2)
	assert(delta_H.shape == (200, 6))

	delta_a = delta_H[:, :-1] * ( 1 - H**2)
	assert(delta_a.shape == (200, 5))

	delta_W1 = np.dot(delta_a.T,  X_full)
	assert(delta_W1.shape == (5, 3))

	
	## 串起来
	eps = 1e-15
	n_epochs = 20000
	learning_rate = 0.01
	hidden_units = 5

	W1, W2, probs = train(X, Y , hidden_units=hidden_units, eps = 1e-15, n_epochs = 20000, learning_rate = 0.01)




