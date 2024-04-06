from Include import*

def get(string: str, index: int):
	if 0 <= index < len(string):
		return string[index]
	return -1

def readPreprocess(file_path: str):
	raw_data = open(file_path, "r", -1, "utf-8").read()
	while '(*' in raw_data:
		raw_data = raw_data[:raw_data.find('(*')] + raw_data[raw_data.find("*)") + 2:]
	while '\n' in raw_data:
		raw_data = raw_data[:raw_data.find('\n')] + " " + raw_data[raw_data.find('\n') + 1:]
		
	result = raw_data.split("\n")
	for i, line in enumerate(result):
		tokens = line.split()
		if len(tokens) > 0 and tokens[0] == "let":
			result[i] = result[i].replace(".", "'.'")

	return "\n".join(result)

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

	for i, line in enumerate(lines):
		tokens = line.split()
		if len(tokens) > 0:
			if tokens[0] == "let":
				if tokens[2] != "=":
					print(f"line({i}) let statement has erroneous '=' sign: {line}")
					return False
			elif tokens[0].startswith("let") and "=" in line:
				print(f"line({i}) let statement spacing error: {line}")
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
						print(f"line({i}) Warning: rule '{tokens[0]}' has no {{return}} statement: {line}")
					if len(tokens) == 1:
						print(f"line({i}) Warning: rule '{tokens[0]}' has no {{return}} statement: {line}")
			break
		if len(tokens) > 0:
			if tokens[0] == "let" and tokens[2] != "=":
				print(f"line({i}) let statement has erroneous '=' sign: {line}")
				return False
			if tokens[0] == "rule":
				parsing_rules = True
				if tokens[1] != "tokens":
					print(f"line({i}) rule tokens =  has erroneous tokens: {line}")
					return False
				elif tokens[2] != "=":
					print(f"line({i}) rule tokens =  has erroneous '=' sign: {line}")
					return False

	return True