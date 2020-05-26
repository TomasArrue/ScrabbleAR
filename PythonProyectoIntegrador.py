def imprimir(matriz):               # funcion para imprimir el tablero mostrando solo la letra
    for x in range(len(matriz)):
        for y in range(len(matriz[x])):
            print("|" + matriz[x][y].letra ,end="")
        print("|",end="")
        print("")

########################### calcular_puntos dani ################################
#def calcular_puntos (letra,multiplier,**kwargs):
#    valor = kwargs[letra]*multiplier
#    return valor
########################### calcular_puntos tom #################################
# mi ideas es guardar todos los modificadores (tuplas) en una lista e ir sumando el valor de la letra 


########################## NO APLICA A UNA MATRIZ DE OBJETOS CELDA ################################################
#CARGAR_CELDA   permite "cargar por valor" una celda //reemplaza todos los valores
#def cargar_celda(dic):
#    nue_dic = {}       #usa un auxiliar para perder la direc de memoria de la celda que quieres copiar y que no se modifique todo
#    for key, dato in dic.items():# key es la llave del elemento del dic y dato es la info correspondiente
#        nue_dic[key] = dato      # carga dato a dato en el dic auxiliar
#    return nue_dic               # retorna la info de la celda con la dirc de memoria del aux  para que el diccionario que pasa como parametro no se modifique
######################################################################################################

ejes = 5    #tamaño de la matriz ejes X ejes

celda_vacia = {"cararter" : "_", #o "c" o "a".etc  # el caracter permanece vacio hasta que se cargue una letra
               "modificador" : ("",0) #si en la celda hay un modificador lo guarda para procesarlo cuando la palabra este lista # este modificador es una tupla donde guarda la operacion aritmetica como un stirng y la segunda el operando
               #tanto el operando como el operador permaneceran vacios si esta celda no posee modificador
              }
#print(celda_vacia) #test de celda_vacia

#esta cargar se rompe #matriz = [[cargar_celda(celda_vacia)] * ejes for i in range(ejes)] #crea la matriz cargando celda vacia

#este cargar no puede fallar

#cargarlo sin la funcion CARGAR_CELDA soluciono problemas de llamado a key
tablero= [[None] * ejes for i in range(ejes)] # carga el tablero en "null" ---> None

for x in range(len(tablero)):
    for y in range(len(tablero[x])):
        tablero[x][y] = Celda()       # pisa el objeto None con un objeto celda //cada uno deberia tener su propia 

#imprimir

imprimir(tablero)

#modifico una celda
print("modifico una casilla")
tablero[1][1].set_letra("A")
imprimir(tablero)

#vacio el tablero
print("vacio el tablero")
tablero[1][1].set_letra(" ")
imprimir(tablero)




# ahora trabajaremos con un ejemplo para procesar los puntos de una palabra sin multiplicadores en las celdas

#######  este metodo resulta util sea objeto o no  ########################
def validar_letra(letra): # este metodo valida la letra para no cargar un carcter que no sea una letra
    cararteres_habilitados = ["A","B","C","D","E","F","G","H","I","J","K","L","N","M","O","P","Q","R","S","T","U","V","W","X","Y","Z","LL","RR"] # no hay decicion tomada sobre "LL" y "RR" se los agrega por ahora
    ok = False
    cont = 0
    while cont <= len(cararteres_habilitados) and ok == False:
        if cararteres_habilitados[cont] == letra:
            ok = True
        cont = cont +1
    return ok
##########################################################################

def ingresar_letra():
    print("Ingrese una letra //'LL' y 'RR' cuentan como un letra ")
    print("si la letra es 'None' la palabra termina")
    letra = str(input()).upper()    
    if(letra != "None"):   # descarta "None" para saber si es el fin
        while not validar_letra(letra):   # en caso de ingresar un caracter in valido
            print("ERROR  ---> LETRA INVALIDA")
            print("Ingrese una letra //'LL' y 'RR' cuentan como un letra ")
            print("si la letra es 'None' la palabra termina")
            letra = str(input()).upper() 
        return letra
    else:
        return letra

def ingresar_coordenada (eje):
    print("Ingrese la coordenada entre: 1 y " + str(eje))
    coord = int(input()) - 1
    while coord < eje  and cood >= 0: # en caso de ingresar una coordenada invalida 
        print("ERROR  ---> COORDENADA INVALIDA")
        print("Por favor ingrese un un numero entre 1 y " + str(eje))
        coord = input()
    return coord

letra = ingresar_letra()
print("===============================================================================")
print("Coordenada Eje X " , end= "")
x = ingresar_coordenada(ejes)
print("===============================================================================")
print("Coordenada Eje Y " , end= "")
y = ingresar_coordenada(ejes)

puntas_totales = 0        # almacena los puntos totales que obtiene la palabra
multiplicar_palabra = 1   # en caso de un modificador que multiplique el total de puntos de la palabra
lista_caracteres = []     # nuestra lista de caracteres es nuestro backroll
while letra != "None":
    while tablero[x][y].letra != " ": # este while verifica que la las coordenadas del tablero esten disponibles
        print("===============================================================================")
        print("ERROR  ---> ESPACIO NO DISPONIBLE")
        print("Por favor ingrese coordenadas que no esten ocupadas")
        print("Coordenada Eje X" , end= "")
        x = ingresar_coordenada(ejes)
        print("Coordenada Eje Y" , end= "")
        y = ingresar_coordenada(ejes)

    tablero[x][y].set_letra(letra) #carga la letra en el tablero

    tupla_carcter = (x,y,letra) ###### no estoy seguro de guardar la letra todavia
    lista_caracteres.append(tupla_carcter) 
    tupla_result = tablero[x][y].procesar_celda(puntas_totales,multiplicar_palabra) # esta tupla duvuelve el resultado de puntos hasta el momento y en caso de encontrar un multiplicador de palabra lo suma
    
    puntas_totales = tupla_result[0]
    multiplicar_palabra = tupla_result[1]

    print("===============================================================================")
    print("Cnatidad de puntos hasta el momento: " + str(puntas_totales))
    print("Multiplicar puntos por: " + str(multiplicar_palabra))
    imprimir(tablero)

    print("===============================================================================")
    print("Siguiente letra")
    letra = ingresar_letra()
    if letra != "None":
        print("===============================================================================")
        print("Coordenada Eje X" , end= "")
        x = ingresar_coordenada(ejes)
        print("Coordenada Eje Y" , end= "")
        y = ingresar_coordenada(ejes)


print("===============================================================================")
print("El resultado final es: " + str(puntas_totales * multiplicar_palabra))


# ahora trabajaremos con un ejemplo para procesar los puntos de una palabra sin multiplicadores en las celdas
print("===============================================================================")
print("Limpia el tablero")

for x,y,_ in lista_caracteres:
    tablero[x][y].letra = " "

imprimir(tablero)
