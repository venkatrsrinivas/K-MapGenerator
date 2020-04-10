'''
Takes An Expression From Infix Notation To Prefix Notation.
For example, it will take: 
(A & B) => and(A, B)
'''

import sys
from pythonds.basic import Stack	
from tkinter import messagebox

#Basic Tree Structure For Expression:
#Run w/ Basic Command 
class TreeNode(object):
	"""docstring for TreeNode"""
	def __init__(self, value):
		#Store Node Value + Left + Right Pointers.
		self.value = value
		self.left = None
		self.right = None 

	#Basic Helper Function To Print Subtree Rooted At self.
	def printTree(self):
		if(self == None):
			return
		print(self.value)
		self.left.print()
		self.right.print()

	def convertToHLD(self):
		#Base Case:
		if(self == None):
			return ""
		#Initialize Current Output Expression:
		output = ""
		#Case 1: Operator.
		if(isOperator(self.value)):
			#Respective STR Based On Operator.
			if(self.value == '&'):
				output += "and("
			elif(self.value == '|'):
				output += "or("
			elif(self.value == '='):
				output += "iff("
			elif(self.value == '>'):
				output += "if("
			elif(self.value == '~'):
				output += "not("
			
			#Negation Does Not Have Left Value.
			#By Definition/Construction of Expression Tree, 
			#Negation Nodes Only Have Left Children.
			if(self.value != "~"):
				output += self.right.convertToHLD()
			if(self.value != "~"):
				output += ", "
			output += self.left.convertToHLD()
			output += ")"
		else:
			#Should Be Alpha Atomic Statement/Variable.
			output += self.value
		return output

#Obtain Associativity of Operator.
def getAssociativity(c):	
	if(c == '&'):
		return 'L'
	elif(c == '|'):
		return 'L'
	elif(c == '='):
		return 'L'
	elif(c == '>'):
		return 'L'
	elif(c == '~'):
		return 'R'
	else:
		return 'L'
   
#Used By infixToPostfix().
#Determines if c is Valid Operator.
def isOperator(c):
	#All Boolean Logic Operators.
	if(c == '&'):
		return True
	elif(c == '|'):
		return True
	elif(c == '='):
		return True
	elif(c == '>'):
		return True
	elif(c == '~'):
		return True
	#Default Case: 
	else:
		return False

#Used By infixToPostfix().
#Determines Precedence of c.
def getPrecedence(c):
	#Respective Operator Precedence.
	if(c == '&'):
		return 2
	elif(c == '|'):
		return 1
	elif(c == '='):
		return 0
	elif(c == '>'):
		return 0
	elif(c == '~'):
		return 4
	#Default Case:
	else:
		return -1

#Run Shunting-Yard Algorithm By Edgar Dijkstra.
def infixToPostfix(infix):
	#infix = '(' + infix + ')'  
	#Initialize Stack.
	opStack = Stack() 
	output = ""
	#print(infix)
	#Loop Through All Tokens:
	for token in infix:
		#Case 1: Operator.
		if(isOperator(token)):
			while(not(opStack.isEmpty())
				and isOperator(opStack.peek())
				and ((getAssociativity(token) == 'L' and getPrecedence(opStack.peek()) >= getPrecedence(token))
					or (getAssociativity(token) ==  'R' and getPrecedence(opStack.peek()) > getPrecedence(token)))):
				output += opStack.peek()
				opStack.pop()
			opStack.push(token)   
		#Case 2: Left Paranthesis.
		elif(token == '('):
			opStack.push(token)
		#Case 3: Right Paranthesis.
		elif(token == ')'):
			while(not(opStack.isEmpty()) and opStack.peek() != '('):
				output += opStack.peek()
				opStack.pop()
			#Error-Checking:
			if(opStack.isEmpty()):
				print("Empty Stack.")
				print(output)
				return "ERROR"
			if(opStack.peek() == '('):
				opStack.pop()
		else:
			#Check For Non-Alpha Characters:
			if(not(token.isalpha())):
				print("Not Alpha Not Space:", token, ".")
				return "ERROR"
			output += token
	#Append All Remaining Characters From opStack.
	while(not(opStack.isEmpty())):
		if(opStack.peek() == '(' or opStack.peek() == ')'):
			print("Uh-OH! Mismatched Paranthesis")
			return "ERROR"
		output += opStack.peek()
		opStack.pop()
	#Return Output.
	return output

#Convert Infix Notation STR To Prefix Notation STR:
def convertInfixToPrefix(infix):
	infix = infix.replace(" ", "")	
	infix = infix.replace("\n", "")
	infix = formatSpecialOperators(infix)
	infix = infix[::-1]
	for k in range(0, len(infix)):
		if(infix[k] == '('):
			infix = infix[:k] + ')' + infix[k+1:]
		elif(infix[k] == ')'):
			infix = infix[:k] + '(' + infix[k+1:]		
	prefix = infixToPostfix(infix) 
	prefix = prefix[::-1]
	return prefix

#Formatting For Biconditional/Conditional Operators:
def formatSpecialOperators(infix):
	infix = infix.replace("<->", "=")
	infix = infix.replace("->", ">")
	return infix

#Convert To Tree:
def convertToTree(postfix):
	#If Output convertInfixToPrefix Returned "ERROR" + Postfix = "RORRE".
	if(postfix == "RORRE"):
		return
	#Initialize Stack.
	convertToTree = Stack()
	for k in range(0, len(postfix)):
		#Case 1: Operator + Not-Negation
		if(isOperator(postfix[k]) and postfix[k] != "~"):
			#Pop Previous One TreeNode.
			prevOne = None
			if(not(convertToTree.isEmpty())):
				prevOne = convertToTree.peek()
				convertToTree.pop()
			#Pop Previous Two TreeNode.
			prevTwo = None
			if(not(convertToTree.isEmpty())):
				prevTwo = convertToTree.peek()
				convertToTree.pop()
			#Create + Set New TreeNode.
			currentNode = TreeNode(postfix[k])
			currentNode.left = prevTwo
			currentNode.right = prevOne
			convertToTree.push(currentNode)
		#Case 2: Operator + Negation.
		elif(isOperator(postfix[k]) and postfix[k] == "~"):
			#Pop Previous One TreeNode.
			prevOne = None
			if(not(convertToTree.isEmpty())):
				prevOne = convertToTree.peek()
				convertToTree.pop()
			#Create + Set New TreeNode.
			currentNode = TreeNode(postfix[k])
			currentNode.left = prevOne 
			convertToTree.push(currentNode)
		#Case 3: New Leaf Node.
		else:
			currentNode = TreeNode(postfix[k])
			convertToTree.push(currentNode)

	#Assert Only Root:
	if(convertToTree.size() != 1):
		print("Error In Construction. Must Review Input/Output.")
	#Set New Head Value = Top/Root of Stack.
	return convertToTree.peek()

#Main Driver Code:
def main(inputValue):
    try:
        currentExpression = inputValue
        prefixValue = convertInfixToPrefix(currentExpression)
        print("Prefix Expression:", prefixValue)
        currentRoot = convertToTree(prefixValue[::-1])
        finalExpression = currentRoot.convertToHLD()
        print(finalExpression)
        return finalExpression
    except:
        messagebox.showerror("Error", "Failed to parse expression. Make sure you answer syntax is correct.")

if __name__ == '__main__':
	if(len(sys.argv) >= 2):     
		inputValue = str(sys.argv[1])
		main(inputValue)
