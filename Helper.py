from Include import*

def get(string: str, index: int):
	if 0 <= index < len(string):
		return string[index]
	return -1

def readPreprocess(file_path: str):
	result = open(file_path, "r", -1, "utf-8").read()
	while '(*' in result:
		result = result[:result.find('(*')] + result[result.find("*)") + 2:]
	while '\n' in result:
		result = result[:result.find('\n')] + " " + result[result.find('\n') + 1:]
	return result

def isLetter(char: str):
	char = ord(char)
	return (char >= 65 and char <= 90) or (char >= 97 and char <= 122)

def isNumber(char: str):
	char = ord(char)
	return char >= 48 and char <= 57

def cleanString(string: str):
	cleaned_string = ' '.join(string.split())
	parts = cleaned_string.split('"')
	for i in range(1, len(parts), 2):
		parts[i] = parts[i].replace(' ', '_')
	result = '"'.join(parts)
	return result

def errorCheck(file_path: str):
	result = open(file_path, "r", -1, "utf-8").read()
	while '(*' in result:
		result = result[:result.find('(*')] + result[result.find("*)") + 2:]
	lines = result.split("\n")
	b_open = 0
	b_close = 0
	for char in result:
		if char == "{": b_open += 1
		if char == "}": b_close += 1
	if b_open != b_close:
		print("Error: Unbalanced Brackets: {}")
		return False
	b_open = 0
	b_close = 0
	for char in result:
		if char == "(": b_open += 1
		if char == ")": b_close += 1
	if b_open != b_close:
		print("Error: Unbalanced Brackets: ()")
		return False
	b_open = 0
	b_close = 0
	for char in result:
		if char == "[": b_open += 1
		if char == "]": b_close += 1
	if b_open != b_close:
		print("Error: Unbalanced Brackets: []")
		return False
	b_open = 0
	for char in result:
		if char == "'": b_open += 1
	if b_open %2 != 0:
		print("Error: Unbalanced Apostrophes: '")
		return False
	b_open = 0
	for char in result:
		if char == '"': b_open += 1
	if b_open %2 != 0:
		print('Error: Unbalanced Apostrophes: "')
		return False

	parsing_rules = False
	for i, line in enumerate(lines):
		tokens = line.split()
		if parsing_rules:
			lines = lines[i:]
			for i, line in enumerate(lines):
				tokens = line.strip().split()
				if len(tokens) > 0:
					if tokens[0] == "|" and len(tokens) < 2:
						print(f"Warning: rule '{tokens[0]}' has no {{return}} statement")
					if len(tokens) == 1:
						print(f"Warning: rule '{tokens[0]}' has no {{return}} statement")
			break
		if len(tokens) > 0:
			if tokens[0] == "let" and tokens[2] != "=":
				print("let statement has erroneous '=' sign")
				return False
			if tokens[0] == "rule":
				parsing_rules = True
				if tokens[1] != "tokens":
					print("rule tokens =  has erroneous tokens")
					return False
				elif tokens[2] != "=":
					print("rule tokens =  has erroneous '=' sign")
					return False

	return True