from Include import *

from Structs import *

def shuntingYard(infix: List[Token]):
	stack: List[Token] = []
	postfix: List[Token] = []
	for char in infix:
		if char.data == '(' and char.isOperator == True: stack.append(char)
		elif char.data == ')' and char.isOperator == True:
			while stack[-1].data != '(' and stack[-1].isOperator == True:
				postfix.append(stack.pop())
			stack.pop()
		elif char.data in PRECEDENCE and char.isOperator == True:
			while stack and stack[-1].data != '(' and stack[-1].isOperator == True and PRECEDENCE[char.data] <= PRECEDENCE[stack[-1].data]:
				postfix.append(stack.pop())
			stack.append(char)
		else: postfix.append(char)
	while stack: postfix.append(stack.pop())
	return postfix