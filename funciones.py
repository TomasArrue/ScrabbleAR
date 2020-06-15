#import json
#import random
#
#def crear_bolsas(bolsa_de_letras, bolsa_jugador,bolsa_maquina):
#    for i in range(7):
#         letra = random.choice(list(bolsa_de_letras.keys()))
#         bolsa_jugador.append(letra)
#         bolsa_de_letras[letra] = bolsa_de_letras[letra] - 1
#         letra_maquina = random.choice(list(bolsa_de_letras.keys()))
#         bolsa_maquina.append(letra_maquina)
#         bolsa_de_letras[letra_maquina] = bolsa_de_letras[letra_maquina] - 1
#
#def pedir_letras(bolsa_de_letras, bolsa_jugador):
#    max = 5
#    cantidad_a_pedir = max - len(bolsa_jugador)
#    for i in range(cantidad_a_pedir):
#        letra = random.choice(list(bolsa_de_letras.keys()))
#        bolsa_jugador.append(letra)
#        bolsa_de_letras[letra] = bolsa_de_letras[letra] - 1
#    print(bolsa_jugador)
#
#
#with open("config.json", "r") as f:
#    configuracion = json.load(f)
#
#bolsa_de_letras = configuracion["cantidad_de_letras"]
#
#valor_de_letra = configuracion["valor_por_letra"]
#
#modificador_de_color = configuracion["modificador_de_letra"]
