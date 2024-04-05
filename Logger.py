from Include import *

from AFD import *
from Structs import *

if not os.path.exists("./output"): os.makedirs("./output")
LOGGING = open("./output/log.md", "w", encoding="utf-8")
#LOGGING = None

def initLog():
	if LOGGING:
		LOGGING.write('''<style>
img {
	height: 20vw;
	display: block;
}
.Full {
	height: auto;
}
</style>
''')
		LOGGING.write("# Alejandro Martinez - 21430\n")

def logVariables(variables: Dict[str, str]):
	if LOGGING:
		max_len = 0
		for key, value in variables.items(): max_len = max(max_len, len(key))

		LOGGING.write("## Variables:\n```python\n{")
		for key, value in variables.items():
			key = f"'{key}'"
			LOGGING.write(f"\n\t" + f"{key:{max_len+2}}")
			LOGGING.write(f" : {repr(value)[1:-1]}")
		LOGGING.write("\n}\n```\n")

def logYalex(return_rules: Dict[str, str], variables: Dict[str, str], syntax_tokens: List[Token]):
	if LOGGING:
		max_len = 0
		for key, value in variables.items(): max_len = max(max_len, len(key))

		LOGGING.write("## Compiled Variables:\n```python\n{")

		for key, value in variables.items():
			key = f"'{key}'"
			LOGGING.write(f"\n\t" + f"{key:{max_len+2}}")
			LOGGING.write(f" : {repr(value)[1:-1]}")

		max_len = 0
		for key, value in return_rules.items(): max_len = max(max_len, len(key))

		LOGGING.write("\n}\n```\n## Syntax Tree:\n```\n")
		LOGGING.write(''.join([repr(item.data)[1:-1] for item in syntax_tokens]))
		LOGGING.write("\n```\n## Statements:\n```python\n{")

		for key, value in return_rules.items():
			key = f"'{key}'" if not key.startswith("'") and not key.endswith("'") else key
			LOGGING.write(f"\n\t" + f"{key:{max_len+2}}")
			LOGGING.write(f" : {repr(value.strip())[1:-1]}")
		LOGGING.write("\n}\n```")

def logPostfix(postfix: List[Token]):
	LOGGING.write("\n## Postfix:\n```\n")
	for token in postfix:
		LOGGING.write(repr(token.data)[1:-1])
	LOGGING.write('\n```')

def logAFD(tree: Node[Token[str]], variables: Dict[str, str]):
	LOGGING.write("\n## AFD:\n```\n")
	def print_tree(tree: Node[Token[str]]):
		if tree:
			LOGGING.write(repr(tree.data.data)[1:-1])
			print_tree(tree.left)
			print_tree(tree.right)
	print_tree(tree)

	LOGGING.write("\n```\n## Variable Syntax Trees:\n")

	for key, value in variables.items():
		LOGGING.write(f"| *{key}* ")
	LOGGING.write("|\n")
	for key, value in variables.items():
		LOGGING.write("|:---:")
	LOGGING.write('|\n')
	for key, value in variables.items():
		LOGGING.write(f'| <img src="./{key}.png"> ')
	LOGGING.write('\n## Full Syntax Tree:\n<img class="Full" src="./tree.png">')
	LOGGING.write('\n\n## AFD:\n<img class="Full" src="./afd_tree.png">')