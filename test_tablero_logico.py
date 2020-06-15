# python3 test_tablero_logico.py
from celda import Celda
from tablero_logico import Tablero
from palabra import Palabra

def validar_letra(letra): # este metodo valida la letra para no cargar un carcter que no sea una letra
    print("Validando la letra")
    cararteres_habilitados = ["A","B","C","D","E","F","G","H","I","J","K","L","N","M","O","P","Q","R","S","T","U","V","W","X","Y","Z","LL","RR"] # no hay decicion tomada sobre "LL" y "RR" se los agrega por ahora
    ok = False
    cont = 0
    while cont <= len(cararteres_habilitados) and ok == False:
        if cararteres_habilitados[cont] == letra:
            ok = True
            print("Letra validada")
        cont = cont +1
    if not ok:
        print("Letra invalidada")
    return ok

def ingresar_letra():
    print("Ingresar letra")
    print("Ingrese una letra //'LL' y 'RR' cuentan como un letra ")
    print("si la letra es 'None' la palabra termina")
    letra = str(input()).upper()
    if(letra != "NONE"):   # descarta "None" para saber si es el fin
        while not validar_letra(letra):   # en caso de ingresar un caracter in valido
            print("ERROR  ---> LETRA INVALIDA")
            print("Ingrese una letra //'LL' y 'RR' cuentan como un letra ")
            print("si la letra es 'none' la palabra termina")
            letra = str(input()).upper()
        print("La letra es: " + letra)
        return letra
    else:
        return letra

def validar_coord(coord, eje = 15):
    print("Validando la coordenada")
    if coord > -1:
        if coord < eje+1:
            print("Coordenada validada")
            return True
        else:
            print("Coordenada invalidada")
            return False
    else:
        print("Coordenada invalidada")
        return False

def ingresar_coordenada (eje = 15):
    print("Ingresar coordenada")
    print("Ingrese la coordenada entre: 1 y " + str(eje))
    coord = int(input())
    coord = coord
#    while validar_coord(coord): # en caso de ingresar una coordenada invalida
#        print("ERROR  ---> COORDENADA INVALIDA")
#        print("Por favor ingrese un un numero entre 1 y " + str(eje))
#        coord = int(input())
    return coord

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
    palabra.restar(tupla_puntos)                            # resta los puntos de la celda
    letra = tablero.get_letra(coord[0], coord[1])           # guarda la letra para devolverla al atril
    tablero.borrar_letra(coord[0], coord[1])                # borra finalmente la letra del tablero
    return letra                                           # retorna la letra para devolverla en el atril

def cargar_dato():# !!!!! esto lo dan los botones luqui
    print("Primero carguemos una letra")
    letra = ingresar_letra()
    print("")
    print("Segundo cargamos las coordenadas")
    x = ingresar_coordenada()
    print("coord x: " + str(x))
    print("")
    y = ingresar_coordenada()
    print("coord y: " + str(y))
    print("")
    print("la letra es "+str(letra)+" y las coordenadas son ("+str(x)+","+str(y)+")")
    return (letra,x,y)

# variables ejemplificadoras
var_tablero = Tablero() #objeto tablero
var_palabra = Palabra() #objeto palabra
x = 0                   #coord
y = 0                   #coord
letra = ""              #letra
var_tablero.cargar_colores()

var_tablero.imprimir()
print("==========================================================================================")
print("Inicia testeo:")
print("")
datos = cargar_dato() # !!!!! esto lo dan los botones luqui
print("Vamos a cargarla:")
cargar_letra(var_palabra, var_tablero, datos[1], datos[2], datos[0])
var_tablero.imprimir()
print("Puntos actuales: "+str(var_palabra.get_puntos() * var_palabra.get_multiplicador_palabra()))
print("==========================================================================================")
print("endique la siguiente operacion: C(cargar)/B(borrar) // Para finalizar escriba 'none'")
operacion = str(input()).upper()
while operacion != "NONE":
    if operacion == "C":
        print("Operacion Cargar")
        datos = cargar_dato()
        print("Vamos a cargarla:")
        cargar_letra(var_palabra, var_tablero, datos[1], datos[2], datos[0])
    elif operacion == "B":
        print("Operacion Borrar")
        if var_palabra.tamnio_lista_coord() != 0:
            print("la letra borrada fue: "+ borrar_letra(var_palabra, var_tablero))
        else:
            print("no hay letra para borrar")
    var_tablero.imprimir()
    print("Puntos actuales: "+str(var_palabra.get_puntos() * var_palabra.get_multiplicador_palabra()))
    print("==========================================================================================")
    print("endique la siguiente operacion: C(cargar)/B(borrar) // Para finalizar escriba 'none'")
    operacion = str(input()).upper()
print("finaliza el testeo")
