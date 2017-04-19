import itertools

def line2type(line):
	return [(i+1)*int(line[i]/abs(line[i])) for i in range(len(line))]
	
def whole_comb(n):
	row = [ [(l*n + i+1)*(comb.count(i)*2 - 1) for i in range(n) \
			]
			for num in range(n+1) \
			for comb in itertools.combinations(range(n), num) \
			for l in range(n) \
		]
	
	col = [ [(i*n + r+1)*(comb.count(i)*2-1) for i in range(n)
			]
			for num in range(n+1) \
			for comb in itertools.combinations(range(n), num) \
			for r in range(n)
		]

	return (row + col)

def txt2dimacs(Input = 'Input.txt', Output = 'Output.dimacs'):
	f = open(Input, 'r')
	n = int(f.readline())
	data = f.read()
	f.close()
	
	pdata = []
	data_ = data.replace('\n', '')
	for i in range(len(data_)):
		if data_[i] is '1':
			pdata = pdata + [[i+1]]
		elif data_[i] is '0':
			pdata = pdata + [[-(i+1)]]			

	wc = whole_comb(n)
	T = int(len(wc)/(2*n))
	
	# same number of 1's and 0's
	count_pos = [len([i for i in line if i > 0]) for line in wc]
	cond_one = [[-p for p in wc[i]] for i in range(len(count_pos)) if count_pos[i] != int(n/2)]

	# compat comb
	cc = [wc[i] for i in range(len(count_pos)) if count_pos[i] == int(n/2)]
	T_ = int(len(cc)/(2*n))

	# no three consecutive 1's and 0's.
	# cond_two = [[-p for p in l] for l in wc for i in range(n-2) \
		# if (l[i]<0 and l[i+1]<0 and l[i+2]<0) or (l[i]>0 and l[i+1]>0 and l[i+2]>0)
		# ]
	cond_two = [[-p for p in l] for l in cc for i in range(n-2) \
		if (l[i]<0 and l[i+1]<0 and l[i+2]<0) or (l[i]>0 and l[i+1]>0 and l[i+2]>0)
		]
	
	# compact compact comb
#	print(time.clock())
#	ccc = [l for l in cc if cond_two.count(l) is 0 ]
#	T__ = int(len(ccc)/(2*n))
#	print(time.clock())
	
	# no same line.
	# cond_three = [[-p for p in wc[i + t*n] + wc[j + t*n]] \
				# for t in range(T) \
				# for (i,j) in itertools.combinations(range(n), 2) \
				# ]
				# + [[-p for p in wc[T*n + i + t*n] + wc[T*n + j + t*n]] \
				# for t in range(T) \
				# for (i,j) in itertools.combinations(range(n), 2) \
				# ]
	cond_three = [[-p for p in cc[i + t*n] + cc[j + t*n]] \
				for t in range(T_) \
				for (i,j) in itertools.combinations(range(n), 2) \
				] \
				+ [[-p for p in cc[T_*n + i + t*n] + cc[T_*n + j + t*n]] \
				for t in range(T_) \
				for (i,j) in itertools.combinations(range(n), 2) \
				]
	# cond_three = [[-p for p in ccc[i + t*n] + ccc[j + t*n]] \
				# for t in range(T__) \
				# for (i,j) in itertools.combinations(range(n), 2)
				# ] \
				# + [[-p for p in ccc[T__*n + i + t*n] + ccc[T__*n + j + t*n]] \
				# for t in range(T__) \
				# for (i,j) in itertools.combinations(range(n), 2) \
				# ]
	
	cond = cond_one + cond_two + cond_three

	__cnf = pdata + cond
	_cnf = [' '.join([str(j) for j in l]) for l in __cnf]
	cnf = ' 0\n'.join(_cnf) + ' 0'

	data_dimcs = 'p cnf ' + str(n*n) + ' ' + str(len(__cnf)) + '\n' + cnf + '\n'
	
	f = open(Output, 'w')
	f.write(data_dimcs)
	f.close()

k = [3, 3, 2, 1, 1]
for i in range(5):
	for j in range(k[i]):
		n = str(i*2+6) + '-' + str(j+1)
		txt2dimacs(n + '.in', n + '.dimacs')
