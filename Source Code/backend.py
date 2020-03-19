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

	def getDistinctVariables(self):
		return self.children;


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

	def getDistinctVariables(self):
		allExpressionVariables = [];
		for k in range(0, len(self.children)):
			currentChild = self.children[k];
			if(currentChild != None):
				for currentVariable in currentChild.getDistinctVariables():
					if(currentVariable != None):
						if(not (currentVariable.value in allExpressionVariables)):
							allExpressionVariables.append(currentVariable.value);
		return allExpressionVariables;

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

# Log base 2 
def Log2(x):
 	return (math.log10(x)/math.log10(2))

# Function to check 
# if x is power of 2 
def isPowerOfTwo(n): 
 	return (math.ceil(Log2(n)) == math.floor(Log2(n)))

class KarnaughMap():
 	#Constructor For KarnaughMap
 	def __init__(self, allExpressionVariables):
 		self.allExpressionVariables = allExpressionVariables;
 		self.totalNumVariables = len(allExpressionVariables);
 		self.xTotalBits = math.floor(self.totalNumVariables/2);
 		self.yTotalBits = math.ceil(self.totalNumVariables/2);
 		self.rows = pow(2, self.xTotalBits);
 		self.columns = pow(2, self.yTotalBits);
 		self.matrix = [[0 for m in range(self.columns)] for k in range(self.rows)];
 		# groupings will be represented as a list of tuples where we have the coordinates of the top left nad bottom right
 		self.groupings = [] 

 	def setOneValues(self, allOneValues):
 		for currentOneValue in allOneValues:
 			currentX, currentY = currentOneValue[self.yTotalBits:], currentOneValue[0:self.yTotalBits];
 			xIndex, yIndex = self.strToIndex(currentX), self.strToIndex(currentY);
 			#print(xIndex, " ", yIndex);
 			self.matrix[xIndex][yIndex] = 1;

 	#Note: Needs To Be Rewritten To Account For Only Changing One Bit
 	#That is, for >= 5 variables!
 	def strToIndex(self, input):
 		if(len(input) == 0):
 			return 0;
 		if(len(input) == 1):
 			return int(input);
 		allTwoVariableData = ["00","01","11","10"]
 		return allTwoVariableData.index(input)
 		# resultIndex = 0;
 		# tempInput = input;
 		# currentExponent = len(tempInput)-1;
 		# while(len(tempInput) != 0):
 		# 	currentValue = int(tempInput[0]);
 		# 	resultIndex += (currentValue*pow(2, currentExponent));
 		# 	tempInput = tempInput[1:];
 		# 	currentExponent -= 1;
 		# return resultIndex; 

 	def addNormGrouping(self, topLeft, bottomRight):
 		# Takes in the coordinates and determines if the values
 		# in the grouping is valid
 		# Returns True for good and False for bad
 		x1,y1 = topLeft
 		x2,y2 = bottomRight
 		val = 1
 		good = True
 		for k in range(x1, x2+1):
 			for m in range(y1, y2+1):
 				if not val == self.matrix[k][m]:
 	 	 	 	 	good = False
 	 	 	 	 	break
 			if not good:
 				break
 		if not good:
 			print("Bad grouping: there is a zero in this grouping\n")
 		return good
 	def addWrapUpGrouping(self, topLeft, bottomRight):
 		# this is the case when BottomRight is Above Top Left
 		# splits the grouping and determines validity of each half
 		x1,y1 = topLeft
 		x2,y2 = bottomRight
 		val = 1
 		good = True
 		L2 = (0, y1)
 		R2 = (self.rows - 1, y2)
 		numberOfBoxes = (x2 + 1 - 0)*(y2 + 1 - y1) + (x2 + 1 - x1)*(self.columns - y1)
 		# groupings must be a power of 2
	 	if not isPowerOfTwo(numberOfBoxes):
 	 	 	print("Bad grouping: Number of Boxes is not a power of two")
 	 	 	return False
 		return self.addNormGrouping(L2, bottomRight) and self.addNormGrouping(topLeft, R2)

 	def addWrapAcrossGrouping(self, topLeft, bottomRight):
 		# This is the case when Top Left is to the right of Bottom Right
 		x1,y1 = topLeft
 		x2,y2 = bottomRight
 		val = 1
 		good = True
 		L2 = (x1, 0)
 		R2 = (x2, self.columns - 1)
 		numberOfBoxes = (x2 + 1 - 0)*(y2 + 1 - y1) + (x2 + 1 - x1)*(self.columns - y1)
 		# groupings must be a power of 2
	 	if not isPowerOfTwo(numberOfBoxes):
 	 	 	print("Bad grouping: Number of Boxes is not a power of two")
 	 	 	return False
 		return self.addNormGrouping(L2, bottomRight) and self.addNormGrouping(topLeft, R2)

 	def addGrouping(self, topLeft, bottomRight):
 		x1,y1 = topLeft
 		x2,y2 = bottomRight
 		valid = True
 		if x1 <= x2 and y1 <= y2:
 			numberOfBoxes = (x2 + 1 - x1)*(y2 + 1 - y1)
 			if not isPowerOfTwo(numberOfBoxes):
	 			print("Bad grouping: Number of Boxes is not a power of two")
			 	valid = False
			 	return
 			valid = self.addNormGrouping(topLeft, bottomRight)
 		elif x1 > x2 and y1 <= y2:
 			valid = self.addUpGrouping(topLeft, bottomRight)
 		elif x1 <= x2 and y1 > y2:
 			valid = self.addAcrossGrouping(topLeft, bottomRight)
 		else:
 			# We can't have Top left be to right and below Bottom Right
 			print("Invalid Grouping: groupings going around the sides cannot be diagonal")
 			valid = False
 		if valid:
 	 	 	group = (topLeft, bottomRight)
 	 	 	if group not in self.groupings:
 	 	 	 	self.groupings.append(group)

 	def removeGrouping(self, topLeft, bottomRight):
 		x1,y1 = topLeft
 		x2,y2 = bottomRight
 		group = (topLeft, bottomRight)
 		if group not in self.groupings:
 			print("Grouping does not exist")
 		else:
 			self.groupings.remove(group)

 	def combineGrouping(self, first, second):
 		tl1, br1 = first
 		tl2, br2 = second
 		newGrouping = first
 		if first in self.groupings and second in self.groupings:
 			self.groupings.remove(first)
 			self.groupings.remove(second)
 			if first == second:
 				print("Both groupings are the same")
 			else:
	 			firstX1, firstY1 = tl1
	 			firstX2, firstY2 = br1
	 			secondX1, secondY1 = tl2
	 			secondX2, secondY2 = br2
	 			if firstX1 == secondX1 and firstX2 == secondX2:
	 				print("Horizontal Combine")
	 				newGrouping = ((firstX1, max(firstY1, secondY1)), (firstX2, max(firstY2, secondY2)))
	 			elif firstY1 == secondY1 and firstY2 == secondY2:
 					print("Vertical Combine")
 					newGrouping = ((max(firstX1, secondX1), firstY1), (max(firstX2, secondX2), firstY2))
 				else:
 					if firstX1 <= secondX1 and firstY1 <= secondY1 and firstX2 >= secondX2 and firstY2 >= secondY2:
 						# First grouping contains second
 						newGrouping = first
 					elif firstX1 >= secondX1 and firstY1 >= secondY1 and firstX2 <= secondX2 and firstY2 <= secondY2:
 						# second grouping contains first
 						newGrouping = second
 					else:
 						print("Invalid Grouping")
	 		self.addGrouping(newGrouping)

 	def printGrouping(self):
 		print(self.groupings)

 	def printMatrix(self):
 		for k in range(0, self.rows):
 			for m in range(0, self.columns):
 				print(self.matrix[k][m], end = " ")
 			print("");

 	def getMatrix(self):
 		return self.matrix;

def main(): 
	#Load Boolean Expressions From Input .txt File:
	if(len(sys.argv) < 2):
		print("Uh-OH!");
		return;
	countLines = 0;
	inputFile = open(sys.argv[1], 'r');
	allKarnaughMaps = []; 
	for inputValue in inputFile:
		#Remove Newline Characters:
		inputValue = inputValue.strip("\n") 
		#Invoke Conversion to CDNF Form:
		resultNormalForm = equivCheck.generate_equivalency(str(inputValue), str(inputValue))[1];
		currentRoot = buildExpressionTreeData(resultNormalForm);
		if(countLines != 0):
			print("");
		print(resultNormalForm)
		print("Pre-Order Traversal:");
		printPreOrder(currentRoot);
		print("Done with Pre-Order Traversal.\n");
		print("Get All Satisfying Values:");
		print(currentRoot.getSatisfyingValues());
		print("Computed All Satisfying Values.\n");
		print("Total # Variables:");
		variables = currentRoot.getDistinctVariables()
		print(variables);
		currentKMap = KarnaughMap(currentRoot.getDistinctVariables());
		currentKMap.setOneValues(currentRoot.getSatisfyingValues());
		currentKMap.printMatrix();
		print("Done w/ Karnaugh Map.");
		countLines += 1;

		
		allKarnaughMaps.append(currentKMap);
	return allKarnaughMaps[0], variables

if __name__ == '__main__':
	main();