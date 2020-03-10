# Quine McCluskey

# Take in a logical expression
# Go through and count the number of variables
# num = 2^{varcount} - 1
# for i in range(num):
# 	if checkTrue(i):
# 		add to list
# make varcount number of tables
# loop through list values and put into tables sorting by number of 1s
# combine values in each adjacent group until nothing to combine left
# spit out remaining indices and convert to binary to find minimized expression

def checkTrue(input, index, variables):
	# Takes in input and then for each variable inputs the value 
	# we have been given in index form and returns truth value
	val = indexTovals(index)
	return false
def indexTovals():
	return None
def countVars(input, variables):
	return 0
def McCluskey(input):
	minterms = []
	variables = []
	varCount = countVars(input, variables)
	num = pow(2, varCount) - 1
	for i in range(num):
		if checkTrue(input, i, variables):
			minterms.append(i)
	tables = [[] for i in range(varCount)]

	# combining
