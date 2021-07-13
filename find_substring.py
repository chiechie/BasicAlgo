
"""
找到一个字符串a中所有的子串,可以跳着取，
下面使用递归算法实现这个功能，算法的时间复杂度为O(n^2)
"""

def find_all_substring(a):
    if len(a) == 1:
        return ["", a]
    len_a = len(a)
    halv = len_a // 2
    left = find_all_substring(a[:halv])
    right =  find_all_substring(a[halv:])
    merge = [l + r for l in left  
                        for r in right]
    return merge
    

if __name__ == "__main__":
    a = "abc"
    results = find_all_substring(a)
    print(len(results), 2**len(a), results)