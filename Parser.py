from Include import *

from Helper import *
from Logger import *
from Structs import *
from Compiler import *

def processVariables(data: str):
	variables: Dict[str, str] = {}
	result: Dict[str, str] = {}
	while 'let' in data:
		index = data.find('let ')
		data = data[index + 3:]
		name = data[:data.find('=')]
		name = cleanString(name)
		if data.find('let ') == -1:
			value = data[data.find('=') + 1: data.find('rule tokens')]
			value = cleanString(value)
			variables[name] = value.replace("\\n", "\n").replace("\\t", "\t")
			data = data[data.find('rule tokens'):]
		else:
			value = data[data.find('=') + 1:data.find('let ')]
			value = cleanString(value)
			variables[name] = value.replace("\\n", "\n").replace("\\t", "\t")
			data = data[data.find('let '):]
	logVariables(variables)
	keys_array = list(variables.keys())
	for key, value in variables.items():
		for ocurrence in keys_array:
			value = compileJoinVariables(value, ocurrence, variables[ocurrence])
		variables[key] = value
	for key, value in variables.items():
		result[key] = processAssignment(value)
	return result

def processRuleTokens(data: str):
	result: List[str] = []
	in_quote = False
	while data != '':
		if 'rule tokens' in data:
			index = data.find('rule tokens')
			data = data[index + 11:]
			rule = cleanString(data[data.find('=' ) + 1:data.find('|')])
			result.append(rule)
			data = data[data.find('|') + 1:]
		else:
			for i, char in enumerate(data):
				if char == "'" or char == '"':
					in_quote = not in_quote
				elif char == '|' and not in_quote:
					rule = cleanString(data[:i])
					result.append(rule)
					data = data[i + 1:]
					break
			else:
				rule = cleanString(data)
				result.append(rule)
				data = ''
	return result

def processReturnRules(rule_tokens: List[str]):
	result: Dict[str, str] = {}
	for rule in rule_tokens:
		if ' {' in rule: result[rule[:rule.find(' {')]] = rule[rule.find(' {') + 2:rule.find('}')]
		else: result[rule] = ''
	return result

def parseToken(token: str):
	stack: List[str] = []
	result: List[Token] = []
	for char in token: stack.append(char)
	while stack:
		char = stack.pop(0)
		if char == "'":
			result.append(Token(stack.pop(0)))
			stack.pop(0)
		elif char in OPERATORS: result.append(Token(char, True))
		else: result.append(Token(char))
	return result

def parseTokens(tokens: List[str]):
	regex = ""
	stack: List[str] = []
	result: List[Token] = []
	regex = "|".join(tokens)
	for char in regex: stack.append(char)
	while stack:
		char = stack.pop(0)
		if char == "'":
			result.append(Token(stack.pop(0)))
			stack.pop(0)
		elif char == '"':
			items = []
			for i in range(len(stack)):
				if stack[i] == '"':
					items.append(stack[i])
					break
				else:
					items.append(stack[i])
			for i in range(len(items)):
				stack.pop(0)
			while items:
				item = items.pop(0)
				if item == '.':
					result.append(Token(item, True))
				elif item != '"':
					result.append(Token(item))
		elif char in OPERATORS:
			result.append(Token(char, True))
		else:
			result.append(Token(char))
	return result