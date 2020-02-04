import sys;
import equivCheck;

class RegularExpressionTreeNode():
	#Constructor For RegularExpressionTreeNode:
	def __init__(self, value):
		self.value = value;
		self.children = [];
	
	def printValue(self):
		print(self.value);


class AndExpressionTreeNode():
	#Constructor For AndExpressionTreeNode:
	def __init__(self):
		self.value = "&";
		self.children = [];

	def printValue(self):
		print(self.value);


class OrExpressionTreeNode():
	#Constructor For OrExpressionTreeNode:
	def __init__(self):
		self.value = "|";
		self.children = [];

	def printValue(self):
		print(self.value);

class NotExpressionTreeNode(RegularExpressionTreeNode):
	#Constructor For NotExpressionTreeNode:
	def __init__(self, value):
		super(NotExpressionTreeNode, self).__init__(value);			

	def printValue(self):
		print("~" + self.value);

				
def printPreOrder(root): 
	if(root != None):
		root.printValue();
		for k in range(0, len(root.children)):
			#print(root.children)
			printPreOrder(root.children[k]);


# def printInOrder(root):
# 	if(root != None):
# 		total = len(root.children);
# 		if(total != 0):
# 			for k in range(0, total-1):
# 				printInOrder(root.children[k]);
# 			print(root.value);
# 			printInOrder(root.children[total-1]);
# 		else:
# 			print(root.value);


def parseAndExpression(start, end, currentExpression):
	newAndTreeNode = AndExpressionTreeNode();
	k = start;
	while(k <= end):
		currentValue = currentExpression[k];
		if(currentValue != "&" and currentValue != "(" and currentValue != ")" and currentValue != " "):
			if(currentValue == "~"):
				newValue = currentExpression[k+1];
				tempNotTreeNode = NotExpressionTreeNode(newValue);
				newAndTreeNode.children.append(tempNotTreeNode);
				k += 1;
			else:
				tempRegularTreeNode = RegularExpressionTreeNode(currentValue);
				newAndTreeNode.children.append(tempRegularTreeNode);
		k += 1;
	newAndTreeNode.children.sort(key = lambda currentExpression: currentExpression.value)
	return newAndTreeNode;

def buildExpressionTreeData(inputNormalForm):
	countOrValues = 0;
	currentRoot = OrExpressionTreeNode();
	for k in range(0, len(inputNormalForm)): 
		#Special Initial Case |: 
		#For First |, Parse AndExpressionData To Left.
		if(inputNormalForm[k] == "|"):
			start = -1;
			end = -1;
			#Store currentLocation To Remember "|" Position:
			currentLocation = k;
			if(countOrValues == 0):
				while(inputNormalForm[k] != ")"):
					k -= 1;
				end = k;
				#Reset Position, k:
				k = currentLocation;
				while(inputNormalForm[k] != "("):
					k -= 1;
				start = k;
				#Reset Position To currentLocation:
				k = currentLocation;
				#Append CurrentAndExpression To Overall OrExpression:
				newAndTreeNode = parseAndExpression(start, end, inputNormalForm);
				currentRoot.children.append(newAndTreeNode);
			#Regular Case |: 
			#Parse AndExpressionData To Right Of | 
			while(inputNormalForm[k] != ")"):
				k += 1;
			end = k;
			#Reset Position To currentLocation:
			k = currentLocation;
			while(inputNormalForm[k] != "("):
				k += 1;
			start = k;
			#Reset Position To currentLocation:
			k = currentLocation;
			#Append CurrentAndExpression To Overall OrExpression:
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
		print("Pre-Order Traversal:");
		printPreOrder(currentRoot);
		print("Done with Pre-Order Traversal.");

if __name__ == '__main__':
	main();