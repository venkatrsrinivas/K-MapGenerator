
'''
Takes An Expression From Infix Notation To Prefix Notation.
For example, it will take: 
(A & B) => and(A, B)
'''

import sys
from pythonds.basic import Stack	

class TreeNode(object):
	"""docstring for TreeNode"""
	def __init__(self, value):
		self.value = value
		self.left = None
		self.right = None 

	def print(self):
		if(self.left != None):
			self.left.print()
		if(self.right != None):
			self.right.print()

	def convertToHLD(self):
		output = "";
		if(isOperator(self.value)):
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
			
			if(self.value != "~"):
				if(self.right != None):
					output += self.right.convertToHLD()
			if(self.left != None):
				if(self.value != "~"):
					output += ", ";
				output += self.left.convertToHLD()
			output += ")"
		else:
			output += self.value
		return output


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
   
def isOperator(c):
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
	else:
		return False

def getPrecedence(c):
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
	else:
		return -1

def infixToPostfix(infix):
	infix = '(' + infix + ')'  
	opStack = Stack() 
	output = ""
	print(infix)
	for k in range(0, len(infix)):
		token = infix[k]
		if(isOperator(token)):
			while(not(opStack.isEmpty())
				and isOperator(opStack.peek())
				and ((getAssociativity(token) == 'L' and getPrecedence(opStack.peek()) >= getPrecedence(token))
					or (getAssociativity(token) ==  'R' and getPrecedence(opStack.peek()) > getPrecedence(token)))):
				output += opStack.peek()
				opStack.pop()
			opStack.push(token)   
		elif(token == '('):
			opStack.push(token)
		elif(token == ')'):
			while(not(opStack.isEmpty()) and opStack.peek() != '('):
				output += opStack.peek()
				opStack.pop()
			if(opStack.isEmpty()):
				print("Empty Stack.")
				print(output)
				return "ERROR"
			if(opStack.peek() == '('):
				opStack.pop()
		else:
			if(not(token.isalpha()) and not(token.isspace())):
				print("Not Alpha Not Space.")
				return "ERROR"
			output += token

	while(not(opStack.isEmpty())):
		if(opStack.peek() == '(' or opStack.peek() == ')'):
			print("Uh-OH!")
			return "ERROR"
		output += opStack.peek()
		opStack.pop()
	return output

def convertInfixToPrefix(infix):
	infix = infix[::-1]
	for k in range(0, len(infix)):
		if(infix[k] == '('):
			infix = infix[:k] + ')' + infix[k+1:]
		elif(infix[k] == ')'):
			infix = infix[:k] + '(' + infix[k+1:]			
	prefix = infixToPostfix(infix.replace(" ", "")) 
	prefix = prefix[::-1]
	return prefix

def convertPrefixToTree(prefix):
	if(prefix == "ERROR"):
		return
	convertToTree = Stack()
	for k in range(0, len(prefix)):
		if(isOperator(prefix[k]) and prefix[k] != "~"):
			prevOne = None
			if(not(convertToTree.isEmpty())):
				prevOne = convertToTree.peek()
				convertToTree.pop()
			
			prevTwo = None
			if(not(convertToTree.isEmpty())):
				prevTwo = convertToTree.peek()
				convertToTree.pop()

			currentNode = TreeNode(prefix[k])
			currentNode.left = prevTwo
			currentNode.right = prevOne
			convertToTree.push(currentNode)

		elif(isOperator(prefix[k]) and prefix[k] == "~"):
			prevOne = None
			if(not(convertToTree.isEmpty())):
				prevOne = convertToTree.top()
				convertToTree.pop()
			currentNode = TreeNode(prefix[k])
			currentNode.left = prevOne 
		else:
			currentNode = TreeNode(prefix[k])
			convertToTree.push(currentNode)

	if(convertToTree.size() != 1):
		print("Error In Construction. Must Review Input/Output.")
	#Set New Head Value = Top/Root of Stack.
	return convertToTree.peek()

currentExpression = str(sys.argv[1])
prefixValue = convertInfixToPrefix(currentExpression)
print(prefixValue)
root = convertPrefixToTree(prefixValue[::-1])
#root.print()
print(root.convertToHLD())

