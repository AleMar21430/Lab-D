from typing import *
import sys

from Structs import *
from AFD import *

TOKENS: Dict[int, str] = "TOKEN_INSERT"

def simular_afd(afd: AFD, simulation_str: str):
	estado_actual = afd.getInitialState()
	estado_aceptado: List[Tuple[State, str]] = []
	cadena_leida = ''
	while len(simulation_str) > 0:
		for char in simulation_str:
			estado_siguiente = estado_actual.getTransitions(char)
			if len(estado_siguiente) > 0 and isinstance(estado_siguiente[0], State):
				cadena_leida += char
				estado_actual = estado_siguiente[0]
				if estado_actual.isFinal:
					estado_aceptado.append((estado_actual, cadena_leida))
			else:
				if estado_aceptado != []:
					token_encontrado = estado_aceptado.pop()
					print(f'{token_encontrado[1]} :: {token_encontrado[0].token.strip().replace("return ", "")}')

					simulation_str = simulation_str[len(token_encontrado[1]):]
					estado_actual = afd.getInitialState()
					cadena_leida = ''
					estado_aceptado = []
					break
				else:
					cadena_leida += char
					print(f'{cadena_leida} :: Lexema no encontrado')
					simulation_str = simulation_str[len(cadena_leida):]
					estado_actual = afd.getInitialState()
					cadena_leida = ''
					break
		if estado_aceptado != []:
			token_encontrado = estado_aceptado.pop()
			print(f'{token_encontrado[1]} :: {token_encontrado[0].token.strip().replace("return ", "")}')
			break