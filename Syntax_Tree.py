from Include import *

from Logger import *
from Structs import *
from Shunting_Yard import shuntingYard

def constructTree(postfix: List[Token]):
	stack: List[Node[Token]] = []
	for char in postfix:
		if not char.isOperator: stack.append(Node(char))
		elif char.data in '*?+':
			node = Node(char)
			if stack: node.left = stack.pop()
			stack.append(node)
		else:
			node = Node(char)
			if stack: node.right = stack.pop()
			if stack: node.left = stack.pop()
			stack.append(node)
	return stack.pop()

def leftMost(root: Node[Token]):
	if root is None: return []
	stack:  List[Node[Token]] = [root]
	result: List[str]  = []
	while len(stack) > 0:
		node = stack.pop(0)
		result.append(str(node))
		if node.left is not None:
			stack.insert(0, node.left)
		if node.right is not None:
			stack.insert(0, node.right)
	return list(reversed(result))
	
def renderTree(root: Node[Token]):
	result = Digraph()
	def traverse(node: Node[Token]):
		if node:
			result.node(str(id(node)), node.data.data)
			if node.left: result.edge(str(id(node)), str(id(node.left)))
			if node.right: result.edge(str(id(node)), str(id(node.right)))
			traverse(node.left)
			traverse(node.right)
	traverse(root)
	return result

def renderSyntaxTree(infix: List[Token], title: str = "tree"):
	if LOGGING:
		tree = constructTree(shuntingYard(infix))
		dot = renderTree(tree)
		dot.render(title, "output", False, True, "png")

def parseToken(token: str):
	stack: List[str] = []
	for char in token: stack.append(char)
	result: List[Token] = []
	while stack:
		char = stack.pop(0)
		if char == "'":
			result.append(Token(stack.pop(0)))
			stack.pop(0)
		elif char in OPERATORS: result.append(Token(char, True))
		else: result.append(Token(char))
	return result

def renderSubTrees(variables: Dict[str, str]):
	if LOGGING:
		for key, value in variables.items():
			renderSyntaxTree(parseToken(value), key)