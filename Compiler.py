from Include import *

from Helper import *

def findIncludeRange(rule):
	include_ranges = []
	for i, char in enumerate(rule):
		if char == "'" and get(rule, i+2) == "'" and get(rule, i+3) == "-" and get(rule, i+4) == "'" and get(rule, i+6) == "'":
			include_ranges.append((rule[i+1], rule[i+5]))
		elif char == "[" and get(rule, i+1) == "^":
			return include_ranges
	return include_ranges

def findExcludeRange(rule):
	enter_negation = False
	exclude_ranges = []
	for i, char in enumerate(rule):
		if enter_negation and char == "'" and get(rule, i+2) == "'" and get(rule, i+3) == "-" and get(rule, i+4) == "'" and get(rule, i+6) == "'":
			exclude_ranges.append((rule[i+1], rule[i+5]))
		elif char == "[" and get(rule, i+1) == "^":
			enter_negation = True
		elif char == "]"and get(rule, i-1) == "'":
			enter_negation = False
	return exclude_ranges

def findIncludeExplicit(rule):
	start_include = False
	include_ranges = []
	for i, char in enumerate(rule):
		if not start_include and char == '"':
			start_include = True
		elif start_include and char == '"':
			start_include = False
		elif char == "[" and get(rule, i+1) == "^":
			break
		elif start_include:
			if char == "\\": include_ranges.append(f".{char}{get(rule, i+1)}")
			elif get(rule, i-1) == "\\": pass
			else: include_ranges.append(char)
	start_include = False
	for i, char in enumerate(rule):
		if not start_include and char == "'" and get(rule, i+2) == "'" and get(rule, i+3) != "-" and get(rule, i-1) != "-" and get(rule, i-2) != "'":
			start_include = True
			include_ranges.append(rule[i+1])
		elif not start_include and char == "'" and get(rule, i+1) == "\\":
			start_include = True
			include_ranges.append(f"\{rule[i+2]}")
		elif start_include and char == "'":
			start_include = False
		elif char == "[" and get(rule, i+1) == "^":
			break
	return include_ranges

def findExcludeExplicit(rule):
	enter_negation = False
	start_exclude = False
	exclude_ranges = []
	for i, char in enumerate(rule):
		if enter_negation and not start_exclude and char == '"':
			start_exclude = True
		elif enter_negation and start_exclude and char == '"':
			start_exclude = False
		elif enter_negation and char == "]" and not start_exclude:
			break
		elif char == "[" and get(rule, i+1) == "^":
			enter_negation = True
		elif start_exclude:
			if char == "\\": exclude_ranges.append(f".{char}{get(rule, i+1)}")
			elif get(rule, i-1) == "\\": pass
			else: exclude_ranges.append(char)
	enter_negation = False
	start_exclude = False
	for i, char in enumerate(rule):
		if enter_negation and not start_exclude and char == "'" and get(rule, i+2) == "'" and get(rule, i+3) != "-" and get(rule, i-1) != "-" and get(rule, i-2) != "'":
			start_exclude = True
			exclude_ranges.append(rule[i+1])
		elif enter_negation and not start_exclude and char == "'" and get(rule, i+1) == "\\":
			start_exclude = True
			exclude_ranges.append(f"\{rule[i+2]}")
		elif enter_negation and start_exclude and char == "'":
			start_exclude = False
		elif enter_negation and char == "]" and not start_exclude:
			break
		elif char == "[" and get(rule, i+1) == "^":
			enter_negation = True
	return exclude_ranges

def getInsideBrackets(text: str):
	start = text.find('[')
	end = text.find(']')
	while start != -1 and end != -1:
		yield text[start + 1:end].strip()
		start = text.find('[', end + 1)
		end = text.find(']', end + 1)

def processAssignment(value: str):
	if value.count("[") > 0 and value.count("[") == value.count("]"):
		matches = getInsideBrackets(value)
		map: Dict[str, str] = {}
		for i, item in enumerate(matches):
			if item[0] == "^":
				last = map.popitem()[1]
				map[f"{last}[{item}]"] = f"[{last}][{item}]"
			else: map[f"[{item}]"] = f"[{item}]"
		for key, val in map.items():
			incl_range = findIncludeRange(val)
			excl_range = findExcludeRange(val)
			incl = findIncludeExplicit(val)
			excl = findExcludeExplicit(val)
			include_list: List[str] = []
			for item in incl_range:
				for i in range(ord(item[0]), ord(item[1])+1):
					include_list.append(chr(i))
			for char in incl:
				include_list.append(char)
			exclude: List[str] = []
			for item in excl_range:
				for i in range(ord(item[0]), ord(item[1])+1):
					exclude.append(chr(i))
			for char in excl:
				exclude.append(char)
			all = [char for char in include_list if char not in exclude]
			map[key] = "[" + "|".join(all) + "]"
		for key, val in map.items():
			value = value.replace(key, val)
		value = value.replace('[', '(')
		value = value.replace(']', ')')
	return value

def validateConcatenation(value: str):
	stack: List[str] = []
	result: str = ""
	for char in value:
		stack.append(char)
	while stack:
		char = stack.pop(0)
		if char == ')':
			if stack:
				if stack[0] not in OPERATORS_CONCAT: result += f"{char}{CONCAT}"

				else: result += char
			else: result += char
		elif char == "'" and stack:
			if len(stack) >= 3:
				if stack[1] == "'":
					if stack[2] not in OPERATORS_CONCAT: result += f"{char}{stack.pop(0)}{stack.pop(0)}{CONCAT}"
					else: result += f"{char}{stack.pop(0)}{stack.pop(0)}"
			elif len(stack) == 2 and stack[1] == "'": result += f"{char}{stack.pop(0)}{stack.pop(0)}"
		elif char == '"' and stack and len(stack) > 2 and stack[2] == '"':
			if stack[2] not in OPERATORS_CONCAT: result += f"{char}{stack.pop(0)}{stack.pop(0)}{stack.pop(0)}{CONCAT}"
			else: result += f"{char}{stack.pop(0)}{stack.pop(0)}{stack.pop(0)}"
		elif char in '*?+':
			if stack:
				if stack[0] not in OPERATORS_CONCAT: result += f"{char}{CONCAT}"
				else: result += char
			else: result += char
		else: result += char
	return result

def compileJoinRuleTokens(return_rules: Dict[str, str], variables: Dict[str, str]):
	stack: List[str] = []
	result: List[str] = []
	for key, value in return_rules.items(): stack.append(cleanString(key))
	for rule in stack:
		for key, value in variables.items():
			if rule == key: rule = value
		result.append(validateConcatenation(f"(({rule})⊡)"))
	return result

def compileJoinVariables(string: str, string_to_replace: str, string_to_replace_with: str):
	variables: List[str] = []
	variable = ""
	result = ""
	for char in string:
		if isLetter(char) or isNumber(char): variable += char
		else:
			if variable != "":
				variables.append(variable)
				variable = ""
			variables.append(char)
	if variable != "": variables.append(variable)
	for variable in variables:
		if variable == string_to_replace: result += string_to_replace_with
		else: result += variable
	return result