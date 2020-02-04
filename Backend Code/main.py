import sys;
import equivCheck;

class RegularExpressionTreeNode():
	#Constructor For RegularExpressionTreeNode:
	def __init__(self, value):
		self.value = value;
		self.children = [];

class AndExpressionTreeNode():
	#Constructor For AndExpressionTreeNode:
	def __init__(self):
		self.value = "&";
		self.children = [];

class OrExpressionTreeNode():
	#Constructor For OrExpressionTreeNode:
	def __init__(self):
		self.value = "|";
		self.children = [];

class NotExpressionTreeNode():
	#Constructor For NotExpressionTreeNode:
	def __init__(self, value):
		self.value = value;
		self.children = [];
				
def printPreOrder(root): 
	if(root != None):
		print(root.value);
		for k in range(0, len(root.children)):
			printPreOrder(root.children[k]);

def printInOrder(root):
	if(root == None):
		return;
	else:
		total = len(root.children);
		if(total != 0):
			for k in range(0, total-1):
				printInOrder(root.children[k]);
			print(root.value);
			printInOrder(root.children[total-1]);
		else:
			print(root.value);


def parseAndExpression(start, end, currentExpression):
	newAndTreeNode = AndExpressionTreeNode();
	for k in range(start, end+1):
		currentValue = currentExpression[k];
		if(currentValue != "&"):
			if(currentValue == "(" or currentValue == ")"):
				continue;
			if(currentValue == "~"):
				k += 1;
				newValue = currentExpression[k];
				tempNotTreeNode = NotExpressionTreeNode(newValue);
				newAndTreeNode.append(tempNotTreeNode);
			else:
				tempRegularTreeNode = RegularExpressionTreeNode(currentValue);
				newAndTreeNode.children.append(tempRegularTreeNode);
	return newAndTreeNode;

def buildExpressionTreeData(inputNormalForm):
	countOrValues = 0;
	currentRoot = OrExpressionTreeNode();
	for k in range(0, len(inputNormalForm)): 
		if(inputNormalForm[k] == "|"):
			currentLocation = k;
			end = -1;
			while(inputNormalForm[k] != ")"):
				k -= 1;
			end = k;
			k = currentLocation;
			start = -1;
			while(inputNormalForm[k] != "("):
				k -= 1;
			start = k;
			k = currentLocation;
			newAndTreeNode = parseAndExpression(start, end, inputNormalForm);
			currentRoot.children.append(newAndTreeNode);
			countOrValues += 1;
	if(countOrValues == 0):
		currentRoot.children.append(parseAndExpression(0, len(inputNormalForm)-1, inputNormalForm));
	return currentRoot;
 

def main(): 
	#Load Boolean Expressions From Input .txt File:
	inputFile = open(sys.argv[1], 'r') 
	for inputValue in inputFile:
		#Remove Newline Characters:
		inputValue = inputValue.strip("\n") 
		#Invoke Conversion to CDNF Form:
		resultNormalForm = equivCheck.generate_equivalency(str(inputValue), str(inputValue))[1];
		currentRoot = buildExpressionTreeData(resultNormalForm);
		print(resultNormalForm)
		print("Pre-Order Tranversal:");
		printPreOrder(currentRoot);
		print(" ");
		print("In-Order Tranversal:");
		printInOrder(currentRoot);
		print(" ");


if __name__ == '__main__':
	main();