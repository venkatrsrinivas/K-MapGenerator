import sys;
import math;
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

	def getSatisfyingValues(self):
		sValue = "";
		for k in range(0, len(self.children)):
			currentChild = self.children[k];
			if(currentChild != None):
				if(isinstance(currentChild, NotExpressionTreeNode)):
					sValue += "0";
				elif(isinstance(currentChild, RegularExpressionTreeNode)):
					sValue += "1";
		return sValue;

	def countDistinctVariables(self):
		return len(self.children);


class OrExpressionTreeNode():
	#Constructor For OrExpressionTreeNode:
	def __init__(self):
		self.value = "|";
		self.children = [];

	def printValue(self):
		print(self.value);

	def getSatisfyingValues(self):
		sValues = [];
		for k in range(0, len(self.children)):
			currentChild = self.children[k];
			if(currentChild != None):
				cValue = currentChild.getSatisfyingValues();
				sValues.append(cValue);
		return sValues;

	def countDistinctVariables(self):
		totalNumVariables = 0;
		for k in range(0, len(self.children)):
			currentChild = self.children[k];
			if(currentChild != None):
				totalNumVariables = max(totalNumVariables, currentChild.countDistinctVariables());
		return totalNumVariables;

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
	newAndTreeNode.children.sort(key = lambda currentExpression: currentExpression.value);
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


class KarnaughMap():
 	#Constructor For KarnaughMap
 	def __init__(self, totalNumVariables):
 		self.xTotalBits = math.floor(totalNumVariables/2);
 		self.yTotalBits = math.ceil(totalNumVariables/2);
 		self.rows = pow(2, self.xTotalBits);
 		self.columns = pow(2, self.yTotalBits);
 		self.matrix = [[0 for m in range(self.columns)] for k in range(self.rows)];

 	def setOneValues(self, allOneValues):
 		for currentOneValue in allOneValues:
 			currentX, currentY = currentOneValue[self.yTotalBits:], currentOneValue[0:self.yTotalBits];
 			xIndex, yIndex = self.strToIndex(currentX), self.strToIndex(currentY);
 			#print(xIndex, " ", yIndex);
 			self.matrix[xIndex][yIndex] = 1;

 	#Note: Needs To Be Rewritten To Account For Only Changing One Bit
 	#That is, for >= 5 variables!
 	def strToIndex(self, input):
 		if(len(input) <= 1):
 			return int(input);
 		allTwoVariableData = ["00","01","11","10"];
 		return allTwoVariableData.index(input);
 		# resultIndex = 0;
 		# tempInput = input;
 		# currentExponent = len(tempInput)-1;
 		# while(len(tempInput) != 0):
 		# 	currentValue = int(tempInput[0]);
 		# 	resultIndex += (currentValue*pow(2, currentExponent));
 		# 	tempInput = tempInput[1:];
 		# 	currentExponent -= 1;
 		# return resultIndex; 

 	def printMatrix(self):
 		for k in range(0, self.rows):
 			for m in range(0, self.columns):
 				print(self.matrix[k][m], end = " ");
 			print("");

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
		print("Done with Pre-Order Traversal.\n");
		print("Get All Satisfying Values:");
		print(currentRoot.getSatisfyingValues());
		print("Computed All Satisfying Values.\n");
		print("Total # Variables:");
		print(currentRoot.countDistinctVariables());
		totalNumVariables = currentRoot.countDistinctVariables();
		currentKMap = KarnaughMap(totalNumVariables);
		currentKMap.setOneValues(currentRoot.getSatisfyingValues());
		currentKMap.printMatrix();

if __name__ == '__main__':
	main();