
"""
reference : https://en.wikipedia.org/wiki/PageRank
"""

def find_all_substring(a):
	a = "abc"

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
	results = find_all_substring(a)
	print(len(results), 2**len(a), results)