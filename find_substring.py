
"""
找到一个字符串a中所有的子串,可以跳着取，
下面使用递归算法实现这个功能，算法的时间复杂度为O(n^2)
"""

def find_not_sucessive_substring(a):
    if len(a) == 1:
        return ["", a]
    len_a = len(a)
    halv = len_a // 2
    left = find_not_sucessive_substring(a[:halv])
    right =  find_not_sucessive_substring(a[halv:])
    merge = [l + r for l in left  
                        for r in right]
    return merge
    

def find_successive_substring(a):
    len_a = len(a) 
    substring = []
    for j in range(1, len_a+1):
        for i in range(len_a - j+1):
            substring.append(a[i : i + j])
    return substring


def get_suffixe_array(a):
    sa = [a[-i:]for i in range(1, len(a)+1)]
    sa = sorted(sa, reverse=False)
    return sa


def get_LCP_array(suffixe_array):
    n = len(suffixe_array)
    LCP = [0] *n
    for i in range(1, n):
        LCP[i] = longestcommon(suffixe_array[i-1], suffixe_array[i])
    return LCP


def longestcommon(s1, s2):
    c = min(len(s1), len(s2))
    res = 0
    for i in range(c):
        if s1[i] != s2[i]:
            return res
        else:
            res += 1
    return res



if __name__ == "__main__":
    a = "abc"
    results1 = find_not_sucessive_substring(a)
    results2 = find_successive_substring(a)

    print(len(results1), 2**len(a), results1)
    print(len(results2), len(a) * (len(a) + 1)//2, results2)

    
    a = "AZAZA"
    SA = get_suffixe_array(a)
    LCP = get_LCP_array(SA)

    print(LCP)
    print(len(a) * (len(a) + 1)//2 - sum(LCP))

    x = "abcd"
    y = "bcad"
    z = "daca"

    T = x + "#"+ y + "$"+ z + "%"
    print(T, get_suffixe_array(T))
    print(get_LCP_array(get_suffixe_array(T)))


