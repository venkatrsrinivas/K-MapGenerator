import sys;
import equivCheck;

def main(): 
	inputFile = open(sys.argv[1], 'r');
	for inputValue in inputFile:
		inputValue = inputValue.strip("\n");
		print(inputValue)
		print(equivCheck.generate_equivalency(str(inputValue), str(inputValue)))

if __name__ == '__main__':
	main();