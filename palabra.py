class Palabra():
    def __init__(self):

        self.coordenadas = []      # una lista de coord de la palabra que cargo actualmente
        self.letras = []  # un diccionario keys coord dato caracter; las keys estan guardadas den coord_letras
        self.sentido = None     # sentido es un boolean que indica si el sentido de la palabra es sentido horizontal true o vertical false
        self.puntos = 0            # guarda los puntos que que va sumando la Palabra

        #en duda
        self.lugar_valido = None   # tupla de coord del espacio habilitado
        self.pos_inicial = None    # la pos_inicial se compone de una tupla para manejar el lugar de la primera letra en la matriz del tablero

    def get_sentido(self):
        return self.sentido

    def set_sentido(self, sentido):
        self.sentido = sentido

    def get_letra(self, x):                       # muestra un letra en una pos
        return self.letras[x]

    def agregar_letra_final(self, letra):         # agrega letra al final
        self.letras.append8(letra)

    def borar_letra_final(self):                  # borra una letra al final y la devuelve
        return self.letras.pop()

    def cant_letras(self):                        # te devuelve la cantidad de letras cargadas
        return len(self.letras())

    def get_coord(self, x):                       # muestra una tupla de coord en una pos
        return self.coordenadas[x]

    def ult_coord(self):                       # muestra la ultima coord
        return self.coordenadas[len(self.coordenadas)]

    def agregar_coord_final(self, coord):         # agrega una tupla de coord al final
        self.coordenadas.append(coord)

    def borrar_coord_final(self):                 # borra una tupla de coord al final y la devuelve
        return self.coordenadas.pop()

    def validar_sentido(self, pos):
        if pos[1] - self.ult_coord()[1] = 1:
            self.set_sentido(True)
        else:
            self.set_sentido(False)


    def validar_lugar(self, pos):
        if self.get_sentido = True:
            if pos[1] - self.ult_coord()[1] = 1:
                return True
            else:
                return False
        else:
            if pos[0] - self.ult_coord()[0] = 1:
                return True
            else:
                return False

    def cargar_letra(self, letra, x, y):          #carga a la letra su coord para procesar la letra
        pos = (x,y)
        if self.cant_letras() == 0:               # si mo hay nada entra de una
            self.agregar_letra_final(letra)
            self.agregar_coord_final(tupla)
            self.sentido = None
        elif 1:
            if validar_lugar(pos):
