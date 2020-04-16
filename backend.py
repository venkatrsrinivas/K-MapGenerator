import sys
import math
import equivCheck
import convert

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

    def getSatisfyingValues(self, isContradiction):
        sValues = [];
        if(not(isContradiction)):
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
        self.allExpressionVariables = allExpressionVariables
        self.totalNumVariables = len(allExpressionVariables)
        self.xTotalBits = math.floor(self.totalNumVariables/2)
        self.yTotalBits = math.ceil(self.totalNumVariables/2)
        self.rows = pow(2, self.xTotalBits)
        self.columns = pow(2, self.yTotalBits)
        self.matrix = [[0 for m in range(self.columns)] for k in range(self.rows)]
        # groupings will be represented as a list of tuples where we have the coordinates of the top left nad bottom right
        self.groupings = [] 

    def setOneValues(self, allOneValues):
        for currentOneValue in allOneValues:
            currentX, currentY = currentOneValue[self.yTotalBits:], currentOneValue[0:self.yTotalBits];
            xIndex, yIndex = self.strToIndex(currentX), self.strToIndex(currentY);
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

    def addNormGrouping(self, topLeft, bottomRight):
        # Takes in the coordinates and determines if the values
        # in the grouping is valid
        # Returns True for good and False for bad
        y1,x1 = topLeft
        y2,x2 = bottomRight
        val = 1
        good = True
        for k in range(y1, y2+1):
            for m in range(x1, x2+1):
                if not val == self.matrix[k][m]:
                    good = False
                    break
            if not good:
                break
        if not good:
            raise Exception("Bad grouping: there is a zero in this grouping")
        return good

    def addWrapUpGrouping(self, topLeft, bottomRight):
         # this is the case when BottomRight is Above Top Left
         # splits the grouping and determines validity of each half
         y1,x1 = topLeft
         y2,x2 = bottomRight
         val = 1
         good = True
         L2 = (0, x1)
         R2 = (self.rows - 1, x2)
         numberOfBoxes = (x2 + 1 - x1)*(y2 + 1) + (x2 + 1 - x1)*(self.rows - y1)
         # groupings must be a power of 2
         if not isPowerOfTwo(numberOfBoxes):
               raise Exception("Bad grouping: Number of Boxes is not a power of two")
               return False
         return self.addNormGrouping(L2, bottomRight) and self.addNormGrouping(topLeft, R2)

    def addWrapAcrossGrouping(self, topLeft, bottomRight):
          # This is the case when Top Left is to the right of Bottom Right
         y1,x1 = topLeft
         y2,x2 = bottomRight
         val = 1
         good = True
         L2 = (y1, 0)
         R2 = (y2, self.columns - 1)
         numberOfBoxes = (x2 + 1)*(y2 + 1 - y1) + (self.columns - x1)*(y2 + 1 - y1)
         # groupings must be a power of 2
         if not isPowerOfTwo(numberOfBoxes):
            raise Exception("Bad grouping: Number of Boxes is not a power of two")
            return False
         return self.addNormGrouping(L2, bottomRight) and self.addNormGrouping(topLeft, R2)

    def addGrouping(self, topLeft, bottomRight, create):
        y1,x1 = topLeft
        y2,x2 = bottomRight
        valid = True

        # Check for corner wraparound case


        if x2 == 0 and y2 == 0 and x1 == self.columns-1 and y1 == self.rows-1 and self.matrix[y2][x2] == 1 and self.matrix[y2][x1] == 1 and self.matrix[y1][x2] == 1 and self.matrix[y1][x1] == 1:
            self.groupings.append("4corners")
            return "Success"

        if x1 > self.columns - 1 or x2 > self.columns - 1 or y1 > self.rows - 1 or y2 > self.rows - 1:
             raise Exception("Indices are greater than bounds")
             valid = False
             return
        if x1 < 0 or x2 < 0 or y1 < 0 or y2 < 0:
             raise Exception("An index is less than zero")
             valid = False
             return
        if y1 <= y2 and x1 <= x2:
            numberOfBoxes = (y2 + 1 - y1)*(x2 + 1 - x1)
            if not isPowerOfTwo(numberOfBoxes):
                valid = False
                raise Exception("Bad grouping: Number of Boxes is not a power of two")
            valid = self.addNormGrouping(topLeft, bottomRight)
        elif y1 > y2 and x1 <= x2:
            valid = self.addWrapUpGrouping(topLeft, bottomRight)
        elif y1 <= y2 and x1 > x2:
            valid = self.addWrapAcrossGrouping(topLeft, bottomRight)
        else:
            # We can't have Top left be to right and below Bottom Right
            raise Exception("Invalid Grouping: groupings going around the sides cannot be diagonal")
            valid = False
        if valid:
            group = (topLeft, bottomRight)
            if group not in self.groupings and create:
                self.groupings.append(group)
        return "Success"

    def removeGrouping(self, topLeft, bottomRight):
        y1,x1 = topLeft
        y2,x2 = bottomRight
        group = (topLeft, bottomRight)
        if group not in self.groupings:
            raise Exception("Grouping does not exist")
        else:
            self.groupings.remove(group)
        return "Success"

    def combineGrouping(self, first, second, merge):
        tl1, br1 = first
        tl2, br2 = second
        newGrouping = first
        remove = []
        if first in self.groupings and second in self.groupings:
            if first == second:
                raise Exception("Both groupings are the same")
            # 4 corner wraparound; currently we have 2 horizontal wraparounds
            elif (tl1 == (0, self.columns-1) and br1 == (0,0) and tl2 == (self.rows-1, self.columns-1) and br2 == (self.rows-1,0)) or (tl2 == (0, self.columns-1) and br2 == (0,0) and tl1 == (self.rows-1, self.columns-1) and br1 == (self.rows-1,0)) or (tl1 == (self.rows-1, 0) and br1 == (0,0) and tl2 == (self.rows-1, self.columns-1) and br2 == (0,self.columns-1)) or (tl2 == (self.rows-1, 0) and br2 == (0,0) and tl1 == (self.rows-1, self.columns-1) and br1 == (0,self.columns-1)):
                newGrouping = ((self.rows-1, self.columns-1), (0, 0))
                remove.append(first)
                remove.append(second)
            else:
                firsty1, firstx1 = tl1
                firsty2, firstx2 = br1
                secondy1, secondx1 = tl2
                secondy2, secondx2 = br2
                if firsty1 == secondy1 and firsty2 == secondy2 and abs(firstx1-secondx1) <= 1 and abs(firstx2-secondx2) <= 1:
                    # print("Horizontal Combine")
                    newGrouping = ((firsty1, min(firstx1, secondx1)), (firsty2, max(firstx2, secondx2)))
                    remove.append(first)
                    remove.append(second)
                elif firsty1 == secondy1 and firsty2 == secondy2 and ((secondx2 == self.columns-1 and firstx1 == 0) or (firstx2 == self.columns-1 and secondx1 == 0)):
                    # print("Horizontal Combine with Wraparound")
                    newGrouping = ((firsty1, max(firstx1, secondx1)), (firsty2, min(firstx2, secondx2)))
                    remove.append(first)
                    remove.append(second)
                elif firstx1 == secondx1 and firstx2 == secondx2 and abs(firsty1-secondy1) <= 1 and abs(firsty2-secondy2) <= 1:
                    # print("Vertical Combine")
                    newGrouping = ((min(firsty1, secondy1), firstx1), (max(firsty2, secondy2), firstx2))
                    remove.append(first)
                    remove.append(second)
                elif firstx1 == secondx1 and firstx2 == secondx2 and ((secondy2 == self.rows-1 and firsty1 == 0) or (firsty2 == self.rows-1 and secondy1 == 0)):
                    # print("Vertical Combine with Wraparound")
                    newGrouping = ((max(firsty1, secondy1), firstx1), (min(firsty2, secondy2), firstx2))
                    remove.append(first)
                    remove.append(second)
                else:
                    if firsty1 <= secondy1 and firstx1 <= secondx1 and firsty2 >= secondy2 and firstx2 >= secondx2:
                        # print("First grouping contains second")
                        newGrouping = first
                        remove.append(second)
                    elif firsty1 >= secondy1 and firstx1 >= secondx1 and firsty2 <= secondy2 and firstx2 <= secondx2:
                        # print("Second grouping contains first")
                        newGrouping = second
                        remove.append(first)
                    else:
                        raise Exception("Invalid Grouping")
            # print("Merging into new grouping: " + str(newGrouping))
            self.addGrouping(newGrouping[0], newGrouping[1], merge)
            if merge:
                for grouping in remove:
                    self.removeGrouping(grouping[0], grouping[1])
        return "Success"

    def printGrouping(self):
        print(self.groupings)

    def getGroupings(self):
        return self.groupings

    def printMatrix(self):
        for k in range(0, self.rows):
            for m in range(0, self.columns):
                print(self.matrix[k][m], end = " ")
            print("");

    def getMatrix(self):
        return self.matrix;
    
    # This function generates a simplified logical expression based on the groupings the user created
    def getExpressionFromGroupings(self):
        expression = ""
        numVars = self.totalNumVariables

        var1 = None
        var2 = None
        var3 = None
        var4 = None

        # Here we hardcode the T/F values for each variable for each coordinate on the K-Map.
        if numVars == 1:
            var1 = [0, 1]
        elif numVars == 2:
            var1 = [[0, 1],[0, 1]]
            var2 = [[0, 0],[1, 1]]
        elif numVars == 3:
            var1 = [[0, 0, 1, 1],[0, 0, 1, 1]]
            var2 = [[0, 1, 1, 0],[0, 1, 1, 0]]
            var3 = [[0,0,0,0],[1,1,1,1]]
        elif numVars == 4:
            var1 = [[0, 0, 1, 1],[0, 0, 1, 1],[0, 0, 1, 1],[0, 0, 1, 1]]
            var2 = [[0, 1, 1, 0],[0, 1, 1, 0],[0, 1, 1, 0],[0, 1, 1, 0]]
            var3 = [[0,0,0,0],[0,0,0,0],[1,1,1,1],[1,1,1,1]]
            var4 = [[0,0,0,0],[1,1,1,1],[1,1,1,1],[0,0,0,0]]
        
        # The final expression will be in DNF. This array will hold all of the disjuncts to be or'd together
        disjunctions = []

        # Iterate through each grouping. For each grouping, we detect which variables change across the grouping
        # and which ones stay the same
        for grouping in self.groupings:
            var1val = None
            var2val = None
            var3val = None
            var4val = None

            y1 = grouping[0][0]
            x1 = grouping[0][1]
            y2 = grouping[1][0]
            x2 = grouping[1][1]

            var1val = var1[y1][x1]
            if numVars > 1:
                var2val = var2[y1][x1]
            if numVars > 2:
                var3val = var3[y1][x1]
            if numVars > 3:
                var4val = var4[y1][x1]
            if x1 <= x2 and y1 <= y2:
                # print("normal")
                # normal grouping, no wraparounds
                for y in range(y1, y2+1):
                    for x in range(x1, x2+1):
                        if var1val != None and var1[y][x] != var1val:
                            var1val = -1
                        if var2val != None and var2[y][x] != var2val:
                            var2val = -1
                        if var3val != None and var3[y][x] != var3val:
                            var3val = -1
                        if var4val != None and var4[y][x] != var4val:
                            var4val = -1
                        
            elif x1 >= x2 and y1 <= y2:
                # print("horiz")
                # horizontal wraparound grouping 
                for y in range(y1, y2+1):
                    for x in range(x1, self.columns):
                        # print(str(y) + "," + str(x))
                        if var1val != None and var1[y][x] != var1val:
                            var1val = -1
                        if var2val != None and var2[y][x] != var2val:
                            # print("Q changed from" + str(var2val) + " to " + str(var2[y][x]))
                            var2val = -1
                        if var3val != None and var3[y][x] != var3val:
                            var3val = -1
                        if var4val != None and var4[y][x] != var4val:
                            var4val = -1
                    for x in range(0, x2+1):
                        if var1val != None and var1[y][x] != var1val:
                            var1val = -1
                        if var2val != None and var2[y][x] != var2val:
                            var2val = -1
                        if var3val != None and var3[y][x] != var3val:
                            var3val = -1
                        if var4val != None and var4[y][x] != var4val:
                            var4val = -1
            elif x1 <= x2 and y1 >= y2:
                # vertical wraparound grouping 
                # print("vert")
                for y in range(y1, self.rows):
                    for x in range(x1, x2+1):
                        if var1val != None and var1[y][x] != var1val:
                            var1val = -1
                        if var2val != None and var2[y][x] != var2val:
                            var2val = -1
                        if var3val != None and var3[y][x] != var3val:
                            var3val = -1
                        if var4val != None and var4[y][x] != var4val:
                            var4val = -1
                for y in range(0, y2+1):
                    for x in range(x1, x2+1):
                        if var1val != None and var1[y][x] != var1val:
                            var1val = -1
                        if var2val != None and var2[y][x] != var2val:
                            var2val = -1
                        if var3val != None and var3[y][x] != var3val:
                            var3val = -1
                        if var4val != None and var4[y][x] != var4val:
                            var4val = -1
            else:
                # what in the world??
                return False, "Internal error, please check manually"

            # print(var1val)
            # print(var2val)
            # print(var3val)
            # print(var4val)

            # This array stores all the conjuncts for this disjunct
            conjunctions = []

            # populate the conjuncts
            if var1val == 1:
                conjunctions.append(str(self.allExpressionVariables[0]))
            if var1val == 0:
                conjunctions.append("~" + str(self.allExpressionVariables[0]))
            if var2val == 1:
                conjunctions.append(str(self.allExpressionVariables[1]))
            if var2val == 0:
                conjunctions.append("~" + str(self.allExpressionVariables[1]))
            if var3val == 1:
                conjunctions.append(str(self.allExpressionVariables[2]))
            if var3val == 0:
                conjunctions.append("~" + str(self.allExpressionVariables[2]))
            if var4val == 1:
                conjunctions.append(str(self.allExpressionVariables[3]))
            if var4val == 0:
                conjunctions.append("~" + str(self.allExpressionVariables[3]))
            
            final = ""
            # conjunct the conjuncts together and add them as a disjunct
            for conjunction in conjunctions:
                final = final + " & " + conjunction
            disjunctions.append(final[3:])

        # disjunct the disjuncts together, the result is the DNF expression
        final = ""
        for disjunction in disjunctions:
            final = final + " | " + "(" + disjunction + ")"
        # print(final[3:])
        return final[3:]

    # This function is responsible for checking a user's answer.
    def check(self):
        valid = True

        # Check whether there are unmerged groupings; ie, two groupings that could be merged.
        # We do this through brute force by attempting to merge every grouping with every other grouping.
        # However, we set a flag so that no changes are actually made to the K-Map.
        for x in self.groupings:
            for y in self.groupings:
                if x is not y and valid:
                    success = ""
                    try:
                        success = self.combineGrouping(x, y, False)
                    except:
                        # groupings x and y could not be merged
                        success = "failed"
                        continue
                    finally:
                        if success != "failed":
                            # we were able to merge two independent groupings, which means user did not merge some groupings
                            # print(x)
                            # print(y)
                            valid = False
                            return False, "Two or more groupings can be merged."

        # Verify that there are no ungrouped 1's remaining in the K-Map
        y = 0
        x = 0
        for row in self.matrix:
            for col in row:
                if col == 1:
                    # find a grouping that contains this cell 
                    contained = False
                    for grouping in self.groupings:
                        y1 = grouping[0][0]
                        x1 = grouping[0][1]
                        y2 = grouping[1][0]
                        x2 = grouping[1][1]
                        if x1 <= x2 and y1 <= y2:
                            # normal grouping, no wraparounds
                            if x >= x1 and x <= x2 and y >= y1 and y <= y2:
                                contained = True 
                                break
                        elif x1 >= x2 and y1 <= y2:
                            # horizontal wraparound grouping 
                            if y >= y1 and y <= y2 and (x >= x1 or x <= x2):
                                contained = True 
                                break
                        elif x1 <= x2 and y1 >= y2:
                            # vertical wraparound grouping 
                            if x >= x1 and x <= x2 and (y >= y1 or y <= y2):
                                contained = True 
                                break
                        else:
                            # what in the world??
                            return False, "Internal error, please check manually"
                    if not contained:
                        return False, "Not all cells are in a grouping"
                x = x + 1
            y = y + 1
            x=0
        # Groupings were made correctly! We now create a logical expression from the groupings.
        expression = self.getExpressionFromGroupings()
        return True, expression

def main(statement): 
    # Process the statement the user inputted
    inputValue = convert.main(statement)

    countLines = 0;
    allKarnaughMaps = []; 
    #Invoke Conversion to CDNF Form:
    outputFromHLDEquiv = equivCheck.generate_equivalency(str(inputValue), str(inputValue), True)
    resultNormalForm = outputFromHLDEquiv[1]
    isContradiction = outputFromHLDEquiv[3]
    currentRoot = buildExpressionTreeData(resultNormalForm);
    if(countLines != 0):
        print("");
    """ print(resultNormalForm)
    print("Pre-Order Traversal:");
    printPreOrder(currentRoot);
    print("Done with Pre-Order Traversal.\n");
    print("Get All Satisfying Values:");
    print(currentRoot.getSatisfyingValues(isContradiction));
    print("Computed All Satisfying Values.\n");
    print("Total # Variables:"); """
    variables = currentRoot.getDistinctVariables()
    # print(variables);
    currentKMap = KarnaughMap(currentRoot.getDistinctVariables());
    currentKMap.setOneValues(currentRoot.getSatisfyingValues(isContradiction));
    currentKMap.printMatrix();
    # print("Done w/ Karnaugh Map.");
    countLines += 1;
    allKarnaughMaps.append(currentKMap);
    return allKarnaughMaps[0], variables, statement # outputFromHLDEquiv[5]

if __name__ == '__main__':
    if(len(sys.argv) >= 2):     
        inputFile = sys.argv[1]
        with open(inputFile) as currentFileReader:
            inputValue = currentFileReader.readline()
            main(inputValue)


