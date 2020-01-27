import sys;
import equivCheck;

def main(): 
	equivCheck.generate_equivalency("A", "not(not(A))")

if __name__ == '__main__':
	main();