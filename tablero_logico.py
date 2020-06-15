from celda import Celda
import json
class Tablero: # tablero es un objeto donde se guardan objetos celdes y sus metodos realizan las operaciones logicas de procesar la informacion
    def __init__(self, ejes = 15):
        self.matriz = [[None] * ejes for i in range(ejes)]  # carga el tablero vacio ---> None
        for x in range(len(self.matriz)):
            for y in range(len(self.matriz[x])):
                self.matriz[x][y] = Celda()       # pisa el objeto None con un objeto celda, cada celda esta vacia

##############################################################################


    #getter y setter
    def get_letra(self, x, y):
        return self.matriz[x][y].get_letra()

    def set_letra(self, x , y, letra):
        self.matriz[x][y].set_letra(letra)

    def get_color(self, x, y):
        return self.matriz[x][y].get_color()

    def set_color(self, x, y, color):
        self.matriz[x][y].set_color(color)

    def get_mod(self, x, y):
        return self.matriz[x][y].get_modificador()

    # otros metodos
    def cargar_colores(self):
        with open('tab.json','r') as t:
            dic_color = json.load(t)
        with open('config.json','r') as m:
            dic_mod = json.load(m)
        dic_mod = dic_mod["modificador_de_letra"]
        tablero_config = dic_color["tab_facil"]
        for colores in tablero_config.keys():
            lista_de_cord = tablero_config[colores]
            mod = dic_mod [colores]
            for par_de_cord in lista_de_cord:
                x,y = par_de_cord
                self.matriz[x][y].set_color(colores)
                self.matriz[x][y].set_modificador((mod[0],mod[1]))

    #""" devuelve un boolean si la celda tiene letra o no """
    def celda_vacia(self, x, y):
        if self.get_letra(x, y) == " ":
            return True
        else:
            return False

    def puntos_celda(self, x, y):
    #""" devuelve los puntos y el multiplicador de palabra en una tupla """
        tupla = self.matriz[x][y].calcular_puntos()
        return tupla

    def cargar_letra(self, x, y, letra):
    #""" recurres al set_letra """
        self.set_letra(x, y, letra)

    def borrar_letra(self, x, y):
    #""" borra la ultima letra """
        self.set_letra(x, y, " ")

    def imprimir(self):
    #""" imprime desde la terminar el tablero """
        for x in range(len(self.matriz)):
            print("|",end="")
            for y in range(len(self.matriz[x])):
                print(self.get_letra(x, y),end="")
                print("|",end="")
            print("")

    def imprimir_color(self):
    #""" imprime desde la terminar el tablero """
        for x in range(len(self.matriz)):
            print("|",end="")
            for y in range(len(self.matriz[x])):
                print(self.get_color(x, y),end="")
                print("|",end="")
            print("")

    def imprimir_mod(self):
    #""" imprime desde la terminar el tablero """
        for x in range(len(self.matriz)):
            print("|",end="")
            for y in range(len(self.matriz[x])):
                print(self.get_mod(x, y),end="")
                print("|",end="")
            print("")
