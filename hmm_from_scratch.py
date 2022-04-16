import numpy as np
from hmmlearn import hmm
np.random.seed(42)


def forward_likelihood(X, pi, A, B, T, N):
    """
    forward algorithm to compute the obeservations' probility

    使用递归的算法，计算T时刻<s_t, obs_1,..., obs_t>出现的概率时，
    借助于上一个时刻的值<s_{t-1}, obs_1, ..., obs_{t-1}>的概率,
    以及转移概率p(s_t | s_{t-1}), 和 观测概率p(obs_{t} | s_t)
    
    返回的是前向似然概率矩阵，
    第0行第t-1列表示: 观测值为(obs_1, obs_2, ..., obs_t), 状态=0的概率

    # pi = np.array([0.2, 0.8])

    # A = np.array([[0.6,0.4],
    #             [0.5, 0.5]])

    # B = np.array([[0.4,0.4,0.2],
    #               [0.3,0.3,0.4],])
    # X = [2,0,2]

    """
    # forward_prob = np.empty((N, T))
    # for s in range(N):
    #     obs1 = X[0].flatten()[0]
    #     forward_prob[s, 0] = pi[s] * emissionprob[s, obs1]
    # for t in range(1, T):
    #     for s in range(N):
    #         tmp = 0
    #         for sp in range(N):
    #             a = transmat[sp, s]
    #             obst = X[t].flatten()[0]
    #             tmp += forward_prob[sp, t-1] * a * emissionprob[s, obst]
    #         forward_prob[s, t] = tmp

    alpha_matrix = np.empty((N, T))
    alpha_matrix[:, 0] = pi * B[:, X[0]]

    # 对于每个时刻t, 计算所有状态的前向概率
    for t in range(1, T):
        # 时刻t的观测值
        obs_t = X[t]
        # 对于t时刻的每个状态，更新前向概率，需要用到上一个时刻的所有状态的前向概率
        for j in range(N):
            alpha_matrix[j , t] = np.sum(alpha_matrix[:, t-1] * A[:,j] * B[j, obs_t])

    return alpha_matrix


def viterbi_decode(X, pi, A, B, T, N):
    """
    使用viterbi算法求解decode问题/推断问题
    # pi = np.array([0.2, 0.8])

    # A = np.array([[0.6,0.4],
    #             [0.5, 0.5]])

    # B = np.array([[0.4,0.4,0.2],
    #               [0.3,0.3,0.4],])
    # X = [2,0,2]
    """
    v_matrix = np.empty((N, T))
    # 对t=1时刻的维特比概率 = 状态初始概率 * 观测概率
    v_matrix[:, 0] = pi * B[:, X[0]]
    best_state = np.argmax(v_matrix[:, 0]).flatten()[0]
    best_state_recorder = [ best_state, ]
    # 对于每个时刻t, 从2到
    for t in range(1, T):
      obs_t = X[t]
      previous_best_state = best_state_recorder[-1]
      previous_best_state_v_prob = v_matrix[previous_best_state, t-1]
      # 对于t时刻的每个状态，更新维特比概率，需要用到上一个时刻的最佳状态
      for j in range(N):
        v_matrix[j , t] =  previous_best_state_v_prob * A[previous_best_state,j] * B[j, obs_t]
      
      best_state = np.argmax(v_matrix[:, t]).flatten()[0]
      best_state_recorder.append(best_state)
      
    print(f"X({X})'s most probable state: ", best_state_recorder)
    return best_state_recorder



if __name__ == "__main__":

    pi = np.array([0.8, 0.2]) 
    A = np.array([[0.6, 0.4], [0.5, 0.5],])
    B = np.array([[.2, .4, .4], [0.5, 0.4, 0.1],])
    X = [2, 0, 2]
    O = 3 # 观测值的种类, 冰淇凌个数
    T = 3 # 观测序列长度
    N = 2 # 隐状态的种类, 天气种类, 0表示天气热，1表示天气冷

    # test for viterbi algorithm
    viterbi_decode(X, pi, A, B, T, N)

    # test for forward algorithm
    forward_prob = forward_likelihood(X, pi, A, B, 1, N)
    likelihood = forward_prob[:, -1].sum()
    assert abs(likelihood - 0.340000) < 0.000001

    forward_prob = forward_likelihood(X, pi, A, B, 2, N)
    likelihood = forward_prob[:, -1].sum()
    assert abs(likelihood - 0.109400)< 0.000001


