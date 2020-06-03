class Celda: #clase celda, parte de la version de dani modificandola

    def __init__(self,letra=" ",modificador = ("+",0)):
        self.letra = letra      # si no usamos el parametro "letra" simepre hubiera cargado  "vacio"
        self.modificador = modificador # si no usamos el parametro "modificador" simepre hubiera cargado  "1" #
                                           # modifico el "modificador" como tupla para darle mas versatilidad al modificador
                                           # un tupla conformada por un operador que pueda sumar "+", restar "-" o multiplicar "*".etc.. y el operando que indica la cantidad 1,2,3...ect
                                                                                                                                #incluso podria estar presente un codigo para multiplicar el valor de la letra y en su defecto de la palabra completa

    # Getter y Setter
    # este Getter modifica independientemente de su valor anterio //proposito: testear y encapsulamiento
    def get_letra(self):
        return self.letra

    # devuelve el valor de letra
    def set_letra(self,letra):
        self.letra = letra

    # este Getter modifica el modificador de puntos
    def get_modificador(self):
        return self.modificador # modificador es una tupla

    # devuelve el valor de modificador
    def set_modificador(self,modificador): # modificador es una tupla
        self.modificador = modificador

    def devolver_valores(self):
        return (self.letra,self.modificador) # se eliminaron los elementos que no se usan: fila, columna y ocupado

    def validar_letra(self,letra): # este metodo valida la letra para no cargar un carcter que no sea una letra
        cararteres_habilitados = ["A","B","C","D","E","F","G","H","I","J","K","L","N","M","O","P","Q","R","S","T","U","V","W","X","Y","Z","LL","RR"] # no hay decicion tomada sobre "LL" y "RR" se los agrega por ahora
        ok = False
        cont = 0
        while cont <= len(cararteres_habilitados) and ok == False:
            if cararteres_habilitados[cont] == letra:
                ok = True
            cont = cont +1
        return ok

    def valida_espacio(self):  # valida el espacio
        return  self.get_letra() == " "

    def cargar_una_letra(self,letra): # carga una letra si no hay nade previamente
        if self.valida_espacio:
            self.set_letra(letra)

    def valor_base(self,):  # busca obtener el valor base propio de la letra:
        ok = False
        cont = 0
        lista_1 = ["A","E","O","S","I","U","N","L","R","T"]
        while cont < len(lista_1) and ok == False:         # 1 punto: A, E, O, S, I, U, N, L, R, T
            if lista_1[cont] == self.get_letra():
                ok = True
                return 1
            cont = cont +1
        cont=0
        lista_2 = ["C","D","G"]
        while cont < len(lista_2) and ok == False:         # 2 puntos: C, D, G
            if lista_2[cont] == self.get_letra():
                ok = True
                return 2
            cont = cont +1
        cont=0
        lista_3 = ["M","B","P"]
        while cont < len(lista_3) and ok == False:        # 3 puntos: M, B, P
            if lista_3[cont] == self.get_letra():
                ok = True
                return 3
            cont = cont +1
        cont=0
        lista_4 = ["F","H","V","Y"]
        while cont < len(lista_4) and ok == False:        # 4 puntos: F, H, V, Y
            if lista_4[cont] == self.get_letra():
                ok = True
                return 4
            cont = cont +1
        cont=0
        lista_5 = ["K","Ñ","Q", "W", "X","LL","RR"]
        while cont < len(lista_5) and ok == False:        # 8 puntos: K, LL, Ñ, Q, RR, W, X
            if lista_5[cont] == self.get_letra():
                ok = True
                return 8
            cont = cont +1
        if ok != True:
            if self.get_letra() == "J":                          # 6 puntos: J
                return 6
            else:                                         # 10 puntos: Z
                return 10

    def procesar_celda (self,puntos, mult): # los puntos representan la cantidad total de puntos sumados por las letras de la palabra hasta el momento y el mult la cantidad de veces que los puntos totales de la palabra se multiplican

        if self.get_modificador()[0] == "+":    # operador de suma
            puntos = puntos + self.get_modificador()[1] + self.valor_base()
        elif self.get_modificador()[0] == "-":  # operador de resta
            puntos = puntos - self.get_modificador()[1] + self.valor_base()
        elif self.get_modificador()[0] == "*":  # operador de multiplicacion de letra
            puntos = puntos + (self.valor_base() * self.get_modificador()[1])
        elif self.get_modificador()[0] == "**": # operador de multiplicacion de palabra
            puntos = puntos + self.valor_base()
            mult = mult + self.get_modificador()[1]
        return (puntos, mult)

######################### FIN DE LA CLASE CELDA #########################################

    def color(self):
        if self.modificador == ("+",0) :
            return "blanco"
        else:
            return "negro"
