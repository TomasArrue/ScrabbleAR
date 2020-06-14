from tablero import Tablero
from palabra import Palabra

var_tablero = Tablero()
var_palabra = Palabra()

def validar

def cargar_una_letra(palabra, tablero, x, y, letra):
""" realiza todas la operaciones de cargar una letra y sumarlos puntos asociados """
# esta funcion ya toma como valido el espacio de celda,
# ejemplo:
# if var_tablero.celda_vacia(x, y):
#     cargar_letra(var_palabra, var_tablero, x, y, letra)
###############################################################################################
# !!!!!!!!!!!! esto podria cambiar y las coords pueden validarse de otra manera !!!!!!!!!!!!!!!
###############################################################################################
    coord = (x, y)                          # guarde las coordenadas en una tupla
    tablero.cargar_letra(x, y, letra)       # carga la letra en el tablero
    tupla_puntos = tablero.sumar(x, y)      # guarda los puntos de la celda en una tupla
    palabra.sumar(tupla_puntos)             # suma los puntos y el multiplicador de palabra
    palabra.agregar_coord_final(coord)      # carga la coordenada al objeto palabra
