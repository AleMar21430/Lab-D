from Include import *

from Helper import *
from Parser import * 
from Logger import *
from Structs import *
from Syntax_Tree import *

YALEX = "./slr-2.yal"
SIMULATION = "hola 123 + ID123 - *"
RENDER = False

# Lab C
if errorCheck(YALEX):
	initLog()

	data            : str              = readPreprocess(YALEX)
	rule_tokens     : List[str]        = processRuleTokens(data)
	return_rules    : Dict[str, str]   = processReturnRules(rule_tokens)
	variables       : Dict[str, str]   = processVariables(data)
	compiled_tokens : List[str]        = compileJoinRuleTokens(return_rules, variables)
	syntax_tokens   : List[Token[str]] = parseTokens(compiled_tokens)

	if RENDER:
		renderSubTrees(variables)
		renderSyntaxTree(syntax_tokens)

	logYalex(return_rules, variables, syntax_tokens)

# Lab D
	from AFD import *
	postfix = shuntingYard(syntax_tokens)
	logPostfix(postfix)
	afd = AFD(postfix, return_rules)
	logAFD(afd.syntax_tree, variables)

	if RENDER: afd.visualizeAFD()

	open('./output/scanner.py', 'w', -1, 'utf-8').write(open('Scanner.py', 'r', -1, 'utf-8').read().replace('"TOKEN_INSERT"', str(return_rules), 1))
	from output.scanner import *
	simular_afd(afd, SIMULATION)