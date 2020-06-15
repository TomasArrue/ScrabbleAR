from celda import Celda

class Tablero: # tablero es un objeto donde se guardan objetos celdes y sus metodos realizan las operaciones logicas de procesar la informacion
    def __init__(self, ejes = 15):
        self.matriz = [[None] * ejes for i in range(ejes)]  # carga el tablero vacio ---> None
        for x in range(len(tablero)):
            for y in range(len(tablero[x])):
                self.matriz[x][y] = Celda()       # pisa el objeto None con un objeto celda, cada celda esta vacia

    #getter y setter
    def get_letra(self, x, y):
        return matriz[x][y].get_letra()

    def set_letra(self, x , y, letra):
        matriz[x][y].set_letra(letra)

    # otros metodos
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
        for x in range(len(tablero)):
            for y in range(len(tablero[x])):
                print("|",end="")
                print(str(self.get_letra(x, y)),end="")
                print("|",end="")
            print("")
