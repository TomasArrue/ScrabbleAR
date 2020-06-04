class Palabra:
    def __init__(self):

        self.coordenadas = []       # una lista de coord de la palabra que cargo actualmente
        self.letras = []            # un diccionario keys coord dato caracter; las keys estan guardadas den coord_letras
        self.sentido = None         # sentido es un boolean que indica si el sentido de la palabra es sentido horizontal true o vertical false
        self.puntos_total = 0       # guarda los puntos que que va sumando la Palabra
        self.puntos_actual = 0      # guarda los puntos de la ultima letra ingresada
        #en duda
        self.lugar_valido = None   # tupla de coord del espacio habilitado
        self.pos_inicial = None    # la pos_inicial se compone de una tupla para manejar el lugar de la primera letra en la matriz del tablero

    def get_puntos_total(self):
        return self.puntos_total

    def set_puntos_total(self, puntos):
        self.puntos_total = puntos

    def get_puntos_actual(self):
        return self.puntos_actual

    def set_puntos_actual(self, puntos):
        self.puntos_actual = puntos

    def sumar_puntos(self):
        self.set_puntos_total(self.get_puntos_total() + self.get_puntos_actual())      # suma los puntos de la letra que se esta procesando

    def restar_puntos(self):
        self.set_puntos_total(self.get_puntos_total() - self.get_puntos_actual())      #!!! resta la letra de la ultima letra procesada util para borrar // IMPORTANTE!!! ESTO AUN PRESENTA ERRORES PARA BORRAR VARIAS VECES SEGUIDASA

    def get_sentido(self):                        # devuelve el sentido de la palabra true horizontal / false vertical /o None no definido
        return self.sentido

    def set_sentido(self, sentido):               # carga el sentido de la palabra
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

    def ult_coord(self):                          # muestra la ultima coord
        return self.coordenadas[len(self.coordenadas)]

    def agregar_coord_final(self, coord):         # agrega una tupla de coord al final
        self.coordenadas.append(coord)

    def borrar_coord_final(self):                 # borra una tupla de coord al final y la devuelve
        return self.coordenadas.pop()

    def validar_sentido(self, pos):
        if pos[1] - self.ult_coord()[1] = 1:      #!!! ejemplo: la ultima letra guardada esta en (1,3) y y la sig (1,4)   se 4 - 3 = da 1 la palabra se carga en horizontal. IMPORTANTE!!! LA VALIDACION DE LA CELDAS Y SENTIDO NO ESTA TERMINADO DE DEFINIR PERO ES UNA RESPONSABILIDAD COMPARTIDA ENTRE EL OBJ TABLERO Y EL OBJ PALABRA PARA QUE LOS MOVIMIENTOS DE LA IA TRABAJE USANDO TABLERO Y PALABRA.
            self.set_sentido(True)          # sentido horizontal
        else:
            self.set_sentido(False)         # sentido vertical

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

    def borrar_puntos(self):
        self.restar_puntos()    # este borrar puntos solo funciona una vez
        self.borrar_coord_final()
        self.borrar_letra_final()

    def cargar_letra(self, letra, x, y, puntos):                #carga a la letra su coord para procesar la letra
        pos = (x,y)                                             #combierte los ejes de coordenadas en una tupla para trabajar
        if self.cant_letras() == 0:                             # si mo hay nada entra de una por que es la primera letra
            self.agregar_letra_final(letra)                     # guarda la letra en la lista de letras
            self.agregar_coord_final(tupla)                     # guarda la coor en la lista de coord
            self.set_sentido(None)                              # pone el sentido en none en caso de borrar y cambiar el sentido de la palabra
        elif self.cant_letras() == 1 and validar_lugar(pos):    # si hay una entra y valida el sentido
            self.validar_sentido(pos)
            self.agregar_letra_final(letra)
            self.agregar_coord_final(tupla)
            self.sumar_puntos()
