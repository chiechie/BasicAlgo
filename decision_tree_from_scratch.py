import numpy as np 
import pandas as pd 
from sklearn.metrics import accuracy_score
from sklearn.datasets import load_iris
from sklearn.tree import DecisionTreeClassifier
from sklearn.tree import export_graphviz
from sklearn.model_selection import train_test_split

pd.options.mode.chained_assignment = None


def gini_index(p):
    return 1 - p**2 - ( 1 - p)**2 

def entropy(p):
    p = 1 - 1e-15 if p > 1 - 1e-15 else p
    p = 1e-15 if p < 1e-15 else p
    return - p * np.log(p) - (1-p) * np.log(1-p)

def infomation_gain(p, p_left,p_right, left_ratio, right_ratio, metric = "gini"):
    if metric == "gini":
        ig = gini_index(p) - left_ratio * gini_index(p_left) -  right_ratio * gini_index(p_right)
    else:
        ig = entropy(p) - left_ratio * entropy(p_left) -  right_ratio * entropy(p_right)
    return ig


def build_stump(X, y):
	"""
	return : tree
	tree 要么是一个value（叶子结点），要么是一个dict，key是question, value是两个子树，
	子树也可以是一个json或者一个value。
	"""
    print("build_stump",)
    n, m = X.shape
    # X_train = X_train.values
    metric = "gini"

    best_splitting_feature = 0
    best_splitting_feature_value = 0
    best_information_gain = 0

    for i in range(m):
        feature = X[:, i]
        for splitting in np.unique(feature):
            left  = y[feature < splitting]
            right = y[feature >= splitting]
            p = 1.0 * y.sum()/ y.size
            p_left = 1.0 * left.sum()/left.size
            p_right = 1.0 *right.sum()/right.size
            left_ratio , right_ratio = 1.0 * left.size/y.size, 1.0 * right.size/y.size
            ig = infomation_gain(p, p_left, p_right, left_ratio, right_ratio, metric)
            if ig >=  best_information_gain:
                best_information_gain = ig
                best_splitting_feature = i
                best_splitting_feature_value = splitting
                
    question = f"feature {best_splitting_feature}  <= {best_splitting_feature_value}"
    print("question", question)
    row_idex = (X[:, best_splitting_feature] <= best_splitting_feature_value)
    
    if row_idex.sum() == 0 or row_idex.sum() == X.shape[0]:
        print("null sub tree, row_idex.shape", row_idex.shape)
        classes, counts = np.unique(y, return_counts=True)
        left_leaf = classes[counts.argmax()]
        return left_leaf
    print("y[row_idex],", y[row_idex].shape)
    classes, counts = np.unique(y[row_idex], return_counts=True)
    left_leaf = classes[counts.argmax()]
    
    classes, counts = np.unique(y[~row_idex], return_counts=True)
    right_leaf = classes[counts.argmax()]
    
    left_tree = build_stump(X[row_idex], y[row_idex])
    right_tree = build_stump(X[~row_idex], y[~row_idex])
    
    if left_tree == right_tree:
        sub_tree = left_leaf
    else:
        sub_tree = {question: [left_tree, right_tree]}
    return sub_tree



if __name__ == "__main__":
	# loading the data set
	dataset = load_iris(as_frame=True)
	X = dataset.data.values
	y = dataset.target.values
	y[y > 0 ] = 1
	y = y.reshape(-1,1)
	rules = build_stump(X, y)
	print(rules)
