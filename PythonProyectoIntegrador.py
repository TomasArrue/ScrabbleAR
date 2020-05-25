class Celda: #clase celda, parte de la version de dani modificandola 

    def __init__(self,letra=" ",multiplicador = ("+",0)):
        self.letra = letra      # si no usamos el parametro "letra" simepre hubiera cargado  "vacio"
        #self.fila = 0          # no se usan nunca 
        #self.columna = 0       # no se usan nunca # ademas estos valores estan presentes el la matriz de tablero
        #self.ocupado = False   # el propio valor de "letra" nos da este resultado. Si "letra" es distinto de " " esta cargado 
        self.multiplicador = multiplicador # si no usamos el parametro "multiplicador" simepre hubiera cargado  "1" #
                                           # modifico el "multiplicador" como tupla para darle mas versatilidad al modificador
                                           # un tupla conformada por un operador que pueda sumar "+", restar "-" o multiplicar "*".etc.. y el operando que indica la cantidad 1,2,3...ect
                                                                                                                                #incluso podria estar presente un codigo para multiplicar el valor de la letra y en su defecto de la palabra completa
    
    # Getter y Setter 
    # este Getter modifica independientemente de su valor anterio //proposito: testear y encapsulamiento
    def get_letra(self):
        return int(self.letra)
    
    # devuelve el valor de letra
    def set_letra(self,letra):
        self.letra = letra
        
    # este Getter modifica el multiplicador de puntos  
    def get_multiplicador(self): 
        return self.multiplicador # multiplicador es una tupla

    # devuelve el valor de multiplicador
    def set_multiplicador(self,multiplicador): # multiplicador es una tupla
        self.multiplicador = multiplicador

    def devolver_valores(self):
        return (self.letra,self.multiplicador) # se eliminaron los elementos que no se usan: fila, columna y ocupado

    def validar_letra(self,letra): # este metodo valida la letra para no cargar un carcter que no sea una letra
        cararteres_habilitados = ["A","B","C","D","E","F","G","H","I","J","K","L","N","M","O","P","Q","R","S","T","U","V","W","X","Y","Z","LL","RR"] # no hay decicion tomada sobre "LL" y "RR" se los agrega por ahora
        ok = False
        cont = 0
        while cont <= len(cararteres_habilitados) and ok == False:
            if cararteres_habilitados[cont] == letra:
                ok = True
            cont = cont +1
        return ok

    def cargar_una_letra(self,letra): # carga una letra si no hay nade previamente
        if self.letra == " ":
            self.set_letra(letra) 
            #self.fila = fila        # no se usa
            #self.columna = columa   # no se usa
            #self.ocupado = True     # no se usa
            
    ############# SIN VERIFICAR 
    def valor_base(self):  # busca obtener el valor base propio de la letra:
        ok = False
        cont = 0
        lista_1 = ["A","E","O","S","I","U","N","L","R","T"] 
        while cont <= len(lista_1) and ok == False:         # 1 punto: A, E, O, S, I, U, N, L, R, T
            if lista_1[cont] == self.get_letra:
                ok = True
                return 1
            cont = cont +1  
        cont=0                                   
        lista_2 = ["C","D","G"]                                        
        while cont <= len(lista_2) and ok == False:         # 2 puntos: C, D, G
            if lista_2[cont] == self.get_letra:
                ok = True
                return 2
            cont = cont +1  
        cont=0                                                         
        lista_3 = ["M","B","P"]                                        
        while cont <= len(lista_3) and ok == False:        # 3 puntos: M, B, P
            if lista_3[cont] == self.get_letra:
                ok = True
                return 3
            cont = cont +1  
        cont=0                                                         
        lista_4 = ["F","H","V","Y"]                                        
        while cont <= len(lista_4) and ok == False:        # 4 puntos: F, H, V, Y
            if lista_4[cont] == self.get_letra:
                ok = True
                return 4
            cont = cont +1  
        cont=0  
        lista_5 = ["K","Ñ","Q", "W", "X","LL","RR"]  
        while cont <= len(lista_5) and ok == False:        # 8 puntos: K, LL, Ñ, Q, RR, W, X
            if lista_5[cont] == self.get_letra:
                ok = True
                return 8
            cont = cont +1                                      
        if ok != True:
            if self.get_letra == "J":                          # 6 puntos: J                          
                return 6
            else:                                         # 10 puntos: Z
                return 10

    ############# SIN VERIFICAR    
    def procesar_celda (self,puntos = 0, mult = 1): # los puntos representan la cantidad total de puntos sumados por las letras de la palabra hasta el momento y el mult la cantidad de veces que los puntos totales de la palabra se multiplican
        if self.multiplicador[0] == "+":    # operador de suma
            puntos = puntos + self.multiplicador[1] + self.valor_base()
        elif self.multiplicador[0] == "-":  # operador de resta
            puntos = puntos - self.multiplicador[1] + self.valor_base()
        elif self.multiplicador[0] == "*":  # operador de multiplicacion de letra
            puntos = puntos + (self.valor_base() * self.multiplicador[1])
        elif self.multiplicador[0] == "**": # operador de multiplicacion de palabra
            puntos = puntos + self.valor_base()
            mult = mult + self.multiplicador[1]
        else: 
            print("ERROR --->   NO SE RECONOSE CARACTER")
        return

    #def devolver_una_letra(self):
    #    return self.letra               # cumple la funcion del setter de letra
    
    #def cargar_un_modificador(self,valor):
    #    self.multiplicador = valor      # cumple la funcion del getter de multiplicador

    #def devolver_multiplicador(self):   
    #    return self.multiplicador       # cumple la funcion del setter de multiplicador

######################### FIN DE LA CLASE CELDA #########################################
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

print("Ingrese una letra //'LL' y 'RR' cuentan como un letra //  no voy a verificar la letra asi que no te equivoques; NO MANDES ALGO QUE NO SEA UNA LETRA")
print("si  letra es 'None' la palabra termina")
letra = str(input())

print("Ingrese la coordenada X entre: 1 y " + ejes)
x = int(input()) - 1
while x < 0 and x > ejes:
    print("ERROR")
    print("Por favor ingrese un un numero entre 1 y " + ejes)
    x = int(input()) - 1

print("Ingrese la coordenada Y entre: 1 y " + ejes)
y = int(input()) - 1
while y < 0 and y > ejes:
    print("ERROR")
    print("Por favor ingrese un un numero entre 1 y " + ejes)
    y = int(input()) - 1

while ()


