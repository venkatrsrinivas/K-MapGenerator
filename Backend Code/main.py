import sys;
import equivCheck;

def main(): 
	inputFile = open(sys.argv[1], 'r') # Load input file, passed as CLI arg for now (will change later)
	for inputValue in inputFile:
		inputValue = inputValue.strip("\n") # remove newline characters
		print(inputValue)
		print(equivCheck.generate_equivalency(str(inputValue), str(inputValue))) # convert expression to CDNF form

if __name__ == '__main__':
	main();