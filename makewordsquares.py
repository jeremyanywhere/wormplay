# use at your own risk. Quick test for two of the different types of gest in the General Intelligence Exam.
#Thoughts, comments, improvements welcome.

import random 
import time

f1 = open ('5letterwords.txt')
rw = f1.read().splitlines() 
word_tree = {}

def populate_tree(word, branch):
	if len(word) == 0:
		return
	if word[0] in branch:
		n = branch[word[0]]
		populate_tree(word[1:len(word)],n)
	else:  # word not in tree yet.
		branch[word[0]]= {}
		populate_tree(word[1:len(word)],branch[word[0]])

def get_matches(tree, pattern, match_list, constructed_word):
	if len(pattern) == 0:
		match_list.append(constructed_word)
		constructed_word=""
	else: 
		if pattern[0] in tree:
			constructed_word+=pattern[0]
			get_matches(tree[pattern[0]],pattern[1:len(pattern)], match_list, constructed_word)
		if pattern[0] == '?':
			for letter in tree:
				get_matches(tree[letter],pattern[1:len(pattern)],match_list, constructed_word+letter)

def dump_string_as_grid(s):
	for i in range(5):
		print(s[i*5:i*5+5])
	print("-----\n")

def match(word, letter, index):
	return word[index] == letter
def get_matching_list(pattern):
	match_list = []
	get_matches(word_tree, pattern, match_list, "")
	return match_list

def get_matching_list_non_recursive(pattern):
	r = range(len(pattern))
	result_list = []
	for w in rw:
		match = True
		for i in r:
			if pattern[i] != '?' and pattern[i] != w[i]:
				match = False
				break
		if match == True:
			result_list.append(w)
	return result_list

def try_next_word(grid, n):
	if (n>9):
		dump_string_as_grid(grid)
		return
	match_list = []
	if (n % 2) == 0: # even, 
		m = ""
		for x in range(5):
			m = m + grid[int(n/2)*5+x]
			match_list = get_matching_list(m)
	if (n % 2) != 0: #pull out verticals
		m = ""
		for x in range(5):
			m = m + grid[int((n-1)/2)+x*5]
			match_list = get_matching_list(m)
	if len(match_list) < 1:  # recursion ends.
		return

	for w in match_list:
		lw = list(grid)
		if (n % 2) == 0: #even
			for x in range(5):
				lw[int(n/2)*5+x] = w[x]
		if (n % 2) != 0: # odd, vertical
			for x in range(5):
				lw[int((n-1)/2)+x*5] = w[x]
		st = ""
		st = st.join(lw)
		#print(st)
		try_next_word(st, n+1)



# random.shuffle(rw)
for w in rw:
	populate_tree(w, word_tree)

ts = time.time()
print(f"added word tree, length of top node:{len(word_tree)}")
match_list = []
p = "??p??"
ts = time.time()
match_list = get_matching_list(p)
print(f"matching {p}, with tree lookup, time taken: {time.time()-ts}ms, match list: {len(match_list)}")

ts = time.time()
match_list = get_matching_list_non_recursive(p)
print(f"matching {p}, with linear list look up, time taken: {time.time()-ts}ms,match list: {len(match_list)}")

for seed in rw:
	print (f"seeding with - {seed}")
	try_next_word(seed+"????????????????????", 1)
print("done.")
