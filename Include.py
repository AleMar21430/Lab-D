from graphviz import Digraph
from typing import *
import os

PLUS = '+'
STAR = '*'
UNION = '|'
CONCAT = '.'
EPSILON = 'ε'
QUESTION = '?'
L_PARENTHESIS = '('
R_PARENTHESIS = ')'

TOKEN = {
	0: 'Return Number'
}

PRECEDENCE = {
	'|' : 1,
	'.' : 2,
	'?' : 3,
	'*' : 3,
	'+' : 3
}

PARENTHESES = [
	L_PARENTHESIS,
	R_PARENTHESIS
]

OPERATORS = [
	PLUS,
	STAR,
	UNION,
	CONCAT,
	EPSILON,
	QUESTION,
	L_PARENTHESIS,
	R_PARENTHESIS
]

OPERATORS_CONCAT = [
	PLUS,
	STAR,
	UNION,
	CONCAT,
	EPSILON,
	QUESTION,
	R_PARENTHESIS
]