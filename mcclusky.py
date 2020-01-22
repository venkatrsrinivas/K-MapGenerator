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