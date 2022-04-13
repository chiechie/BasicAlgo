import numpy as np
from hmmlearn import hmm
np.random.seed(42)

#================benchmark=======

n_components = 2
model = hmm.MultinomialHMM(n_components=n_components)

pi = np.array([0.8, 0.2])
model.startprob_ = pi
print("pi: \n", pi)

transmat = np.array([[0.6, 0.4], [0.5, 0.5],])
model.transmat_  = transmat
print("转移: \n", transmat)

emissionprob = np.array([[.2, .4, .4],
                    [0.5, 0.4, 0.1],] )

model.emissionprob_ = emissionprob
print("emissionprob: \n", emissionprob)

# X 是冰淇淋个数
# Z 是天气，Z
X, Z = model.sample(10)

# print("samples from GMM")
# ice_cream = [x.flatten()[0] + 1 for x in X]
# Z_state = ["COLD" if z==0 else "HOT"for z in Z]
# print("X:", ice_cream)
# print("Z:", Z_state)


# # model.fit(X)
# logprob, pred_Z =  model.decode(X)
# pred_Z_state = ["COLD" if z==0 else "HOT"for z in pred_Z]
# print("pred_Z:", pred_Z_state)


# n_diff = np.sum(abs(np.array(Z) - np.array(pred_Z)))
# print(f"error decoding {n_diff} times, logprob={logprob}", )

#================HMM begin============

# forward algorithm to compute the obeservations' probility

N_state = n_components
# T = 3

X = [2, 0, 2] * 10
X = np.array(X).reshape(-1, 1)


def forward_probality(T, N):
    """
    使用递归的算法，计算T时刻<s_t, obs_1,..., obs_t>出现的概率时，
    借助于上一个时刻的值<s_{t-1}, obs_1, ..., obs_{t-1}>的概率,
    以及转移概率p(s_t | s_{t-1}), 和emision概率p(obs_{t} | s_t)
    
    返回的是前向似然概率矩阵，
    第0行第t-1列表示: 观测值为(obs_1, obs_2, ..., obs_t), 状态=0的概率
    """
    forward_prob = np.empty((N_state, T))
    for s in range(N_state):
        obs1 = X[0].flatten()[0]
        forward_prob[s, 0] = pi[s] * emissionprob[s, obs1]
    for t in range(1, T):
        for s in range(N_state):
            tmp = 0
            for sp in range(N):
                a = transmat[sp, s]
                obst = X[t].flatten()[0]
                tmp += forward_prob[sp, t-1] * a * emissionprob[s, obst]
            forward_prob[s, t] = tmp
    return forward_prob


if __name__ == "__main__":

    forward_prob = forward_probality(1, N_state)
    fprob = forward_prob[:, -1].sum()
    assert abs(fprob - 0.340000) < 0.000001

    forward_prob = forward_probality(2, N_state)
    fprob = forward_prob[:, -1].sum()
    assert abs(fprob - 0.109400)< 0.000001


    for T in range(1, 10):
        forward_prob = forward_probality(T, N_state)
        fprob = forward_prob[:,T-1].sum()
        # print("forward probabilty: \n", forward_prob)
        print(f"obsitions[{T}] 's probility:{fprob:5f} ")

