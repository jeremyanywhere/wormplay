# Generates 

import random 
import time

f1 = open ('commonwords.txt')
rw = f1.read().split() 
file_write = True
if file_write:
	fo = open ("out.txt","w")
word_tree = {}
ts = time.time()

def output(str):
	print(str)
	if file_write:
		fo.write(str+"\n")

def populate_tree(word, branch):
	if len(word) == 0:
		return
	if word[0] in branch:
		n = branch[word[0]]
		populate_tree(word[1:len(word)],n)
	else:  # word not in tree yet.
		branch[word[0]]= {}
		populate_tree(word[1:len(word)],branch[word[0]])

def get_matches(tree, pattern, match_list,constructed_word):
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
	tm = time.time()-ts
	for i in range(5):
		output(s[i*5:i*5+5])
	output("-----\n")
	output(f"----timestamp {tm}-----\n")
	
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

def try_next_word(grid, n, used_set):
	if (n>9):
		dump_string_as_grid(grid)
		output(f"{used_set}")
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
		if w not in used_set:
			lw = list(grid)
			if (n % 2) == 0: #even
				for x in range(5):
					lw[int(n/2)*5+x] = w[x]
			if (n % 2) != 0: # odd, vertical
				for x in range(5):
					lw[int((n-1)/2)+x*5] = w[x]
			st = ""
			st = st.join(lw)
			used_set.add(w)
			try_next_word(st, n+1, used_set)
			used_set.remove(w)

for w in rw:
	populate_tree(w, word_tree)

for seed in rw:
	output (f"seeding with - {seed}")
	try_next_word(seed+"????????????????????", 1, set({}))
output("done.")
if file_write:
	fo.close()
