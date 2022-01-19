# use at your own risk. Quick test for two of the different types of gest in the General Intelligence Exam.
#Thoughts, comments, improvements welcome.

import random 


f1 = open ('5letterwords.txt')
rw = f1.read().splitlines()
# print (f"{rw}")
count = 0
seed = random.choice(rw)
print (f"seed-- {seed}")

def dump_string_as_grid(s):
	for i in range(5):
		print(s[i*5:i*5+5])

def match(word, letter, index):
	return word[index] == letter

def get_matching_list(pattern):
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

def try_next_word(s, n):
	if (n>5):
		dump_string_as_grid(s)
		return
	match_list = []
	if (n % 2) == 0: # even, 
		m = ""
		for x in range(5):
			m = m + s[int(n/2)*5+x]
			match_list = get_matching_list(m)
	if (n % 2) != 0: #pull out verticals
		m = ""
		for x in range(5):
			m = m + s[int((n-1)/2)+x*5]
			match_list = get_matching_list(m)
	if len(match_list) < 1:  # recursion ends.
		return

	for w in match_list:
		lw = list(s)
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


try_next_word(seed+"????????????????????", 1)
