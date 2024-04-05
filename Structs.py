from Include import *

T = TypeVar('T')

class Node(Generic[T]):
	def __init__(self, data: T | None = None, id: int | None = None):
		self.data: T = data
		self.id: int = id

		self.left:  Node[T] | None = None
		self.right: Node[T] | None = None

		self.nullable: bool | None = None
		self.first: Set[Node[T]] | None = set()
		self.last:  Set[Node[T]] | None = set()
		self.next:  Set[Node[T]] | None = set()
		self.queue: List[Set[Node[T]]] = []

	def __str__(self):
		return str(self.data)

class Token(Generic[T]):
	def __init__(self, data: T, isOperator: bool = False):
		self.data: T = data
		self.id: int = ord(data)
		self.isOperator: bool = isOperator

	def __str__(self):
		return str(self.data)

class State:
	def __init__(self, id: int, isFinal = False, token: str = None):
		self.id: int | None = id
		self.isFinal: bool = isFinal
		self.token: str = token
		self.transitions: Dict[str, List[State]] = {}

	def addTransition(self, token: str, state: 'State'):
		if token in self.transitions:
			self.transitions[token].append(state)
		else:
			self.transitions[token] = [state]

	def getTransitions(self, token : str):
		if token in self.transitions:
			return self.transitions[token]
		else:
			return []

	def delTransition(self, token):
		if token in self.transitions:
			del self.transitions[token]

class Transition:
	def __init__(self, token: 'Token[str]', state: State):
		self.token: Token[str] | None = token
		self.state: State | None = state