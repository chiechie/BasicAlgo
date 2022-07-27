"""
异序词(anagram)定义:
一个字符串将字符重排之后，等于另一个字符串，就说两个字符串互为异序词。

异序词检测，即判断两个字符串是否可以通过某种重排得到等价的形式，
异序词检测有3种方法：
1. 先排序，后比较
2. 逐字符比较
3. 比较计数器：计数器的构造可以用list，也可以用dict。使用dict构造计数器时，key既可以是字符，也可以是int。

提升计算效率的方法：
1. 计数器初始化，避免在循环中判断成员是否存在。
2. 循环次数多时，计算指令要尽量少。
3. 计数器可以用list也可以用dict，如果索引可以用来检索内容，比如0，1，2，。。。代表按字母表顺序排列的a，b，c，。。。，优先用list。
适合用list来存储的抽象数据类型还有矩阵。业务场景，一般要按照某个含义的key来读取内容，一般用dict。

效率最高的是：anagram_counter_dict_str_predifined_key
预先定义字典计数器
然后比较两个计数器的分布差异
"""

import timeit


def anagram_sort_and_compare(str1, str2):
	"""
	先排序，后比较
	时间复杂度的，取决于sort，O(nlogn)或者O(n^2)

	"""

	str1 = list(str1)
	str2 = list(str2)

	# 在python中，sort是list特有的方法
	str1.sort()
	str2.sort()

	n_len = len(str1)
	is_same = True

	i = 0
	while i < n_len and is_same:
		if str1[i] == str2[i]:
			i += 1
		else:
			is_same  = False
	return is_same


def anagram_loop(str1, str2):
	"""
	逐字符比较
	时间复杂度为，(n^2)
	字符长度超过1000算不懂

	"""
	str1 = list(str1)
	str2 = list(str2)

	ind_1 = 0
	is_same = True
	n_len = len(str1)

	while ind_1 < n_len and is_same:

		ind_2 = 0
		found = False

		while ind_2 < n_len and not found:
			if str2[ind_1] == str2[ind_2]:
				found = True
				str2[ind_2] = None
			ind_2 += 1

		if found:
			ind_1 = ind_1 + 1
		else:
			is_same = False

	return is_same



def anagram_counter_list(str1, str2):
	"""
	比较计数器的分布,
	使用list来构造计数器

	"""
	container1 = [0] * 26
	for char in str1:
		ind = ord(char) - ord("a")
		container1[ind] = container1[ind] + 1


	container2 = [0] * 26
	for char in str2:
		ind = ord(char) - ord("a")
		container2[ind] = container2[ind] + 1

	is_same = True
	i = 0
	while i < 26 and is_same:
		if container1[i] ==  container2[i]:
			i += 1
		else:
			is_same = False
	return is_same



def anagram_counter_dict_int(str1, str2):
	"""
	比较计数器的分布
	使用dict来构造计数器, 使用int作为key
	"""
	dict1 = {i: 0 for i in range(26)}
	for char in str1:
		ind = ord(char) - ord("a")
		dict1[ind] = dict1[ind] + 1


	dict2 = {i: 0 for i in range(26)}
	for char in str2:
		ind = ord(char) - ord("a")
		dict2[ind] = dict2[ind] + 1

	is_same = True
	i = 0
	while i < 26 and is_same:
		if dict1[i] ==  dict2[i]:
			i += 1
		else:
			is_same = False
	return is_same



def anagram_counter_dict_str(str1, str2):
	"""
	比较计数器的分布
	使用dict来构造计数器，使用原始char作为key
	"""
	dict1 = {}
	for char in str1:
		if char not in dict1:
			dict1[char] = 1
		else:
		 	dict1[char] += 1

	dict2 = {}
	for char in str2:
		if char not in dict2:
			dict2[char] = 1
		else:
		 	dict2[char] += 1

	n_len = len(dict1)
	is_same = True
	i = 0
	keys = list(dict1.keys())
	while i < n_len and is_same:
		k = keys[i]
		if k not in dict2:
			is_same = False
		elif dict1[k] != dict2[k]:
			is_same = False
		i += 1

	return is_same



def anagram_counter_dict_str_predifined_key(str1, str2):
	"""
	比较计数器的分布,
	使用container来构造计数器, 
	计数时，直接对char对应的key赋值

	"""
	char_list = [chr(ord("a")+i) for i in range(26)]
	container1 = {char: 0 for char in char_list}
	for char in str1:
		container1[char] = container1[char] + 1

	container2 = {char: 0 for char in char_list}
	for char in str2:
		container2[char] = container2[char] + 1

	is_same = True
	i = 0
	while i < 26 and is_same:
		if container1[char_list[i]] ==  container2[char_list[i]]:
			i += 1
		else:
			is_same = False
	return is_same



def anagram_solution4(s1, s2):
	"""
	使用list构造计数器，并非最优的方法，
	"""
	c1 = [0] * 26
	c2 = [0] * 26
	for i in range(len(s1)):
		# 逐字符计数时，使用了ord的操作，这个操作，在字符串很长的时候，消耗的时间很多。
		pos = ord(s1[i]) - ord('a') 
		c1[pos] = c1[pos] + 1
	
	for i in range(len(s2)):
		pos = ord(s2[i]) - ord('a')
		c2[pos] = c2[pos] + 1
	j = 0
	still_ok = True
	while j < 26 and still_ok:
		if c1[j] == c2[j]:
			j = j + 1
		else:
			still_ok = False
	return still_ok


if __name__ == "__main__":
	# print(anagram_solution4('apple','pleap'))

	str1 = "askjerterweuyoztuitb"*100000
	str2 = "askjerterweuyoztuitb"*100000
	number = 100
	print(f"compare two str, len={len(str1)}, run {number} times")

	t = timeit.Timer("anagram_sort_and_compare(str1,str2)", "from __main__ import str1, str2, anagram_sort_and_compare")
	lst_time = t.timeit(number=number)
	print("%s cost %.3f milliseconds" % ("anagram_sort_and_compare", lst_time))


	# t = timeit.Timer("is_same_str_loop(str1,str2)", "from __main__ import str1, str2, is_same_str_loop")
	# lst_time = t.timeit(number=number)
	# print("%s cost %.3f milliseconds" % ("is_same_str_loop", lst_time))


	t = timeit.Timer("anagram_counter_list(str1,str2)", "from __main__ import str1, str2, anagram_counter_list")
	lst_time = t.timeit(number=number)
	print("%s cost %.3f milliseconds" % ("anagram_counter_list", lst_time))



	t = timeit.Timer("anagram_counter_dict_int(str1,str2)", "from __main__ import str1, str2, anagram_counter_dict_int")
	lst_time = t.timeit(number=number)
	print("%s cost %.3f milliseconds" % ("anagram_counter_dict_int", lst_time))


	t = timeit.Timer("anagram_counter_dict_str(str1,str2)", "from __main__ import str1, str2, anagram_counter_dict_str")
	lst_time = t.timeit(number=number)
	print("%s cost %.3f milliseconds" % ("anagram_counter_dict_str", lst_time))


	t = timeit.Timer("anagram_counter_dict_str_predifined_key(str1,str2)", "from __main__ import str1, str2, anagram_counter_dict_str_predifined_key")
	lst_time = t.timeit(number=number)
	print("%s cost %.3f milliseconds" % ("anagram_counter_dict_str_predifined_key", lst_time))

	t = timeit.Timer("anagram_solution4(str1,str2)", "from __main__ import str1, str2, anagram_solution4")
	lst_time = t.timeit(number=number)
	print("%s cost %.3f milliseconds" % ("anagram_solution4", lst_time))
