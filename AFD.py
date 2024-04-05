from Shunting_Yard import *
from Include import *
from Structs import *

class AFD:
	def __init__(self, postfix: List[Token], return_rules: Dict[str, str]):
		self.states: Set[State[int]] = set()
		self.initial_states: Set[State[int]] = set()
		self.final_states: Set[State[int]] = set()
		self.syntax_tree: Node[Token[str]] = None

		return_rules = {index : value for index, (key, value) in enumerate(return_rules.items())}
		TOKEN_DICT = return_rules

		self.syntax_tree = treeConstruction(postfix)
		getNullable(self.syntax_tree)
		traverseTree(self.syntax_tree, getNullable)
		getFirstPos(self.syntax_tree)
		getLastPos(self.syntax_tree)
		table = getNextPos(self.syntax_tree)
		sorted_table = sorted(table, key=lambda x: x[0])
		root = self.syntax_tree.first

		root = self.syntax_tree.first
		symbols = getSymbols(sorted_table)
		symbols.remove('⊡')
		state_dict = {}
		transiciones = []
		id = 0
		x = []
		for y in root:
			x.append(y)
		state_dict[id] = x
		id += 1
		visited_states = []
		states_queue = []
		states_queue.append(state_dict[0])
		final = getFinalState(sorted_table)
		while len(states_queue) > 0:
			estado_actual = states_queue.pop()
			visited_states.append(estado_actual)
			for symbol in symbols:
				transition = getTransition(estado_actual, symbol, sorted_table)
				transition = sorted(transition)
				if transition != [] and not None:
					transiciones.append([estado_actual, symbol, transition])
					if transition not in visited_states and transition not in states_queue:
						state_dict[id] = transition
						states_queue.append(transition)
						states_queue = sorted(
							states_queue, reverse=True)
						id += 1
		for key, value in state_dict.items():
			if value == []:
				del state_dict[key]
				break
		transitions = []
		for key, value in state_dict.items():
			for i in transiciones:
				if i[0] == value:
					transitions.append([key, i[1], i[2]])
		for key, value in state_dict.items():
			for i in transitions:
				if i[2] == value:
					i[2] = key

		state_count = []
		for key, value in state_dict.items():
			state_count.append(key)
		state_count = set(state_count)
		for state_id in state_count:
			state = State(state_id)
			for key, value in state_dict.items():
				if key == state_id:
					for val in value:
						if val in final:
							state.isFinal = True
							transition = final.index(val)
							state.token = TOKEN_DICT[transition]
			self.states.add(state)

		for state_id in self.states:
			for transition in transitions:
				if transition[0] == state_id.id:
					state_id.addTransition(transition[1], self.getState(transition[2]))

	def visualizeAFD(self):
		dot = Digraph()
		for state in self.states:
			if state.isFinal:
				dot.node(str(state.id), str(state.id), shape="doublecircle")
			else:
				dot.node(str(state.id), str(state.id))
		for state in self.states:
			for transition in state.transitions:
				for estado_siguiente in state.getTransitions(transition):
					if isinstance(estado_siguiente, State):
						dot.edge(str(state.id), str(estado_siguiente.id), label=transition)
		dot.render("afd_tree", "output", False, True, "png")

	def getState(self, id):
		for state in self.states:
			if state.id == id:
				return state

	def getInitialState(self):
		for state in self.states:
			if state.id == 0:
				return state

def treeConstruction(postfix: List[Token[str]]):
	stack: List[Node[Token[str]]] = []
	id = 0
	for i, char in enumerate(postfix):
		if not char.isOperator:
			if char.data == 'ε':
				stack.append(Node(char, None))
			else:
				stack.append(Node(char, id))
				id += 1
		elif char.data == '*' or char.data == '+' or char.data == '?':
			node = Node(char, None)
			node.left = stack.pop()
			stack.append(node)
		elif char.data == "|" or char.data == ".":
			node = Node(char, None)
			node.right = stack.pop()
			node.left = stack.pop()
			stack.append(node)
	return stack.pop()

def getNullable(root: Node[Token[str]]):
	if root is None:
		return False
	if not root.data.isOperator:
		if root.data.data == 'ε':
			root.nullable = True
		else:
			root.nullable = False
		return False
	if root.data.data == '|':
		nullable = root.left.nullable or root.right.nullable
	elif root.data.data == '.':
		nullable = root.left.nullable and root.right.nullable
	elif root.data.data == '*':
		nullable = True
	elif root.data.data == '+':
		nullable = root.left.nullable
	elif root.data.data == '?':
		nullable = True
	else:
		nullable = False
	root.nullable = nullable
	return nullable or False

def traverseTree(node: Node[Token[str]], func):
	if node is not None:
		traverseTree(node.left, func)
		traverseTree(node.right, func)
		func(node)

def getFirstPos(node: Node[Token[str]]):
	if node:
		if node.left is None and node.right is None:
			node.first.add(node.id)
		elif node.data.data == '.' and node.data.isOperator:
			getFirstPos(node.left)
			getFirstPos(node.right)
			if node.left.nullable:
				node.first = node.left.first.union(node.right.first)
			else:
				node.first = node.left.first
		elif node.data.data == '|' and node.data.isOperator:
			getFirstPos(node.left)
			getFirstPos(node.right)
			if list(node.left.first)[0] == None:
				node.first = node.right.first
			elif list(node.right.first)[0] == None:
				node.first = node.left.first
			else:
				node.first = node.left.first.union(node.right.first)
		elif node.data.data == '*' and node.data.isOperator:
			getFirstPos(node.left)
			node.first = node.left.first
		elif node.data.data == '+' and node.data.isOperator:
			getFirstPos(node.left)
			node.first = node.left.first
		elif node.data.data == '?' and node.data.isOperator:
			getFirstPos(node.left)
			node.first = node.left.first
	if node and node.data.data is not None and node.first is None:
		node.first = node.left.first

def getLastPos(node: Node[Token[str]]):
	if node:
		if node.left is None and node.right is None:
			node.last.add(node.id)
		elif node.data.data == '.' and node.data.isOperator:
			getLastPos(node.left)
			getLastPos(node.right)
			if node.right.nullable:
				node.last = node.left.last.union( node.right.last)
			else:
				node.last = node.right.last
		elif node.data.data == '|' and node.data.isOperator:
			getLastPos(node.left)
			getLastPos(node.right)
			if list(node.left.last)[0] == None:
				node.last = node.right.last
			elif list(node.right.last)[0] == None:
				node.last = node.left.last
			else:
				node.last = node.left.last.union( node.right.last)
		elif node.data.data == '*' and node.data.isOperator:
			getLastPos(node.left)
			node.last = node.left.last
		elif node.data.data == '+' and node.data.isOperator:
			getLastPos(node.left)
			node.last = node.left.last
		elif node.data.data == '?' and node.data.isOperator:
			getLastPos(node.left)
			node.last = node.left.last
	if node and node.data.data is not None and node.last is None:
		node.last = node.right.last

def getNextPos(syntax_tree: Node[Token[str]], state_table: List[List[List[Set]]] = []):
	val = True
	if syntax_tree:
		if syntax_tree.data.data == '.' and syntax_tree.data.isOperator:
			for i in syntax_tree.left.last:
				for k in state_table:
					if k[0] == i:
						k[2].extend(list(syntax_tree.right.first))
						val = False
				if val:
					simbol = getNodeVal(syntax_tree, i)
					state_table.append(
						[i, simbol, list(syntax_tree.right.first)])
		elif syntax_tree.data.data == '*' and syntax_tree.data.isOperator:
			for i in syntax_tree.last:
				for k in state_table:
					if k[0] == i:
						k[2].extend(list(syntax_tree.first))
						val = False
				if val:
					simbol = getNodeVal(syntax_tree, i)
					state_table.append([i, simbol, list(syntax_tree.first)])
		elif syntax_tree.data.data == '+' and syntax_tree.data.isOperator:
			for i in syntax_tree.last:
				for k in state_table:
					if k[0] == i:
						k[2].extend(list(syntax_tree.first))
						val = False
				if val:
					simbol = getNodeVal(syntax_tree, i)
					state_table.append([i, simbol, list(syntax_tree.first)])
		val = False
		for k in state_table:
			if k[0] == syntax_tree.id:
				val = True
		if not val:
			simbol = getNodeVal(syntax_tree, syntax_tree.id)
			state_table.append([syntax_tree.id, simbol, []])
		for i in state_table:
			if i[0] is None:
				state_table.remove(i)
		state_table = getNextPos(syntax_tree.left, state_table)
		state_table = getNextPos(syntax_tree.right, state_table)
	return state_table

def getNodeVal(syntax_tree: Node[Token[str]], id: int):
	if syntax_tree:
		if syntax_tree.id == id:
			return syntax_tree.data.data
		else:
			return getNodeVal(syntax_tree.left, id) or getNodeVal(syntax_tree.right, id)

def getTransition(states: List[State], symbol: str, state_table: List[List[List[Set[int]]]]):
	transitions: List[Set[int]] = []
	for state in states:
		for j in state_table:
			if j[0] == state and j[1] == symbol:
				for k in j[2]:
					if k not in transitions:
						transitions.append(k)
	return transitions

def getSymbols(state_table: List[str]):
	symbols = []
	for state in state_table:
		if state[1] not in symbols:
			symbols.append(state[1])
	return symbols

def getFinalState(state_table: List[str]):
	final_state = []
	for state in state_table:
		if state[1] == '⊡':
			final_state.append(state[0])
	return final_state