from tablero import Tablero
from palabra import Palabra

# variables ejemplificadoras
var_tablero = Tablero() #objeto tablero
var_palabra = Palabra() #objeto palabra
x = 0                   #coord
y = 0                   #coord
letra = "a"             #letra

def cargar_letra(palabra, tablero, x, y, letra):
#""" realiza todas la operaciones de cargar una letra y sumarlos puntos asociados """
# esta funcion ya toma como valido el espacio de celda,
# ejemplo:
# if var_tablero.celda_vacia(x, y):
#     cargar_letra(var_palabra, var_tablero, x, y, letra)
###############################################################################################
# !!!!!!!!!!!! esto podria cambiar y las coords pueden validarse de otra manera !!!!!!!!!!!!!!!
###############################################################################################
    coord = (x, y)                              # guarde las coordenadas en una tupla
    tablero.cargar_letra(x, y, letra)           # carga la letra en el tablero
    tupla_puntos = tablero.puntos_celda(x, y)   # guarda los puntos de la celda en una tupla
    palabra.sumar(tupla_puntos)                 # suma los puntos y el multiplicador de palabra
    palabra.agregar_coord_final(coord)          # carga la coordenada al objeto palabra

def borrar_letra(palabra, tablero):
#""" borra la ultima letra cargada en el tablero y resta sus respectivos puntos"""
    coord = palabra.borrar_coord_final()                    # guarda la coordenada de la ultima letra en la Palabra
    tupla_puntos = tablero.puntos_celda(coord[0], coord[1]) # guarda los puntos de la celda en una tupla
    tablero.restar(tupla_puntos)                            # resta los puntos de la celda
    letra = tablero.get_letra(coord[0], coord[1])           # guarda la letra para devolverla al atril
    tablero.borrar_letra(coord[0], coord[1])                # borra finalmente la letra del tablero
    return letras                                           # retorna la letra para devolverla en el atril
