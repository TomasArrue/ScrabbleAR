from tablero import Tablero
from palabra import Palabra

var_tablero = Tablero()
var_palabra = Palabra()

def validar

def cargar_una_letra(palabra, tablero, x, y, letra):
""" realiza todas la operaciones de cargar una letra y sumarlos puntos asociados """
    coord = (x, y)
    tablero.cargar_letra(x, y, letra)       # carga la letra en el tablero
    tupla_puntos = tablero.sumar(x, y)      # guarda los puntos de la celda en una tupla
    palabra.sumar(tupla_puntos)             # suma los puntos y el multiplicador de palabra
    palabra.agregar_coord_final(coord)      # carga la coordenada al objeto palabra
