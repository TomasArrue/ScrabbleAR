class Celda: #clase celda, parte de la version de dani modificandola

    def __init__(self,letra=" ",modificador = ("+",0), color = " "):
        self.letra = letra      # si no usamos el parametro "letra" simepre hubiera cargado  "vacio"
        self.color = color
        self.modificador = modificador # si no usamos el parametro "modificador" simepre hubiera cargado  "1" #
                                           # modifico el "modificador" como tupla para darle mas versatilidad al modificador
                                           # un tupla conformada por un operador que pueda sumar "+", restar "-" o multiplicar "*".etc.. y el operando que indica la cantidad 1,2,3...ect
                                                                                                                                #incluso podria estar presente un codigo para multiplicar el valor de la letra y en su defecto de la palabra completa

    # Getter y Setter
    def get_letra(self):
        return self.letra

    def set_letra(self,letra):
        self.letra = letra

    def get_color(self):
        return self.color

    def set_color(self, color):
        self.color = color

    def get_modificador(self):
        return self.modificador

    def set_modificador(self,modificador):
        self.modificador = modificador

    # otros metodos
    def cargar_una_letra(self,letra):
    #""" carga una letra si no hay nade previamente """
        if self.valida_espacio:
            self.set_letra(letra)

    def borrar_letra(self):
    #""" borra y devuelve la letra borrada """
        letra = self.get_letra()
        self.set_letra(" ")
        return letra

    def valor_base(self):
    #""" busca obtener el valor base propio de la letra """
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

    def calcular_puntos(self):
    #""" devuelve una tupla donde el primer elemento son los puntos de la celda y el segundo es la cantantidad de multiplicador para puntos de la palabra """
        mult = 0
        if self.get_modificador()[0] == "+":    # operador de suma
            puntos = self.valor_base() + self.get_modificador()[1]
        elif self.get_modificador()[0] == "-":  # operador de resta
            puntos = self.valor_base() - self.get_modificador()[1]
        elif self.get_modificador()[0] == "*":  # operador de multiplicacion de letra
            puntos = self.valor_base() * self.get_modificador()[1]
        elif self.get_modificador()[0] == "**": # operador de multiplicacion de palabra
            puntos = self.valor_base()
            mult = self.get_modificador()[1]
        return (puntos, mult)

######################### FIN DE LA CLASE CELDA #########################################

    def color(self):
        if self.modificador == ("+",0) :
            return "blanco"
        else:
            return "negro"
