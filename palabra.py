class Palabra:
    def __init__(self):
        self.multiplicador_palabra = 1  # indica la cantidad por la cual hay que multiplicar los puntos
        self.lista_coord = []           # una lista de coord de la palabra que cargo actualmente
        self.sentido_horizontal = None             # sentido_horizontal es un boolean que indica si el sentido de la palabra es sentido horizontal true o vertical false
        self.puntos = 0                 # guarda los puntos que que va sumando la Palabra

    # getter y setter
    def get_puntos(self):
        return self.puntos

    def set_puntos(self, puntos):
        self.puntos = puntos

    def get_sentido_horizontal(self):                        # devuelve el sentido de la palabra true horizontal / false vertical /o None no definido
        return self.sentido_horizontal

    def set_sentido_horizontal(self, sentido):               # carga el sentido de la palabra
        self.sentido_horizontal = sentido

    def get_lista_coord(self, x):                       # muestra una tupla de coord en una pos
        return self.lista_coord[x]

    def set_lista_coord(self, x, coord):                       # muestra una tupla de coord en una pos
        return self.lista_coord[x] = coord

    def get_multiplicador_palabra(self):
        return self.multiplicador_palabra

    def set_multiplicador_palabra(self, mul):
        self.multiplicador_palabra = mul

    # otros metodos
    def tamnio_lista_coord(self):
    """ devuelve el tamaño de la lista de coordenadas """
        return len(self.lista_coord)

    def cargar_lista_coord(self, tupla_coord, pos):
    """ carga una tupla de coordenadas en una posicion """
        self.lista_coord[pos] = tupla_coord

    def borrar_lista_coord(self, pos):
    """ borra y devuelve un elemento de la lista de tupla de coordenadas """
        return self.lista_coord.pop(pos)

    def agregar_coord_final(self, coord):
    """ carga una tupla de coordenadas en la ultima posicion """
        self.coordenadas.append(coord)

    def borrar_coord_final(self):
    """ borra y devuelve el ultimo elemento de la lista de tupla de coordenadas """
        return self.coordenadas.pop()

    def validar_sentido(self, pos):
    """  """
        if pos[1] - self.ult_coord()[1] = 1:      #!!! ejemplo: la ultima letra guardada esta en (1,3) y y la sig (1,4)   se 4 - 3 = da 1 la palabra se carga en horizontal. IMPORTANTE!!! LA VALIDACION DE LA CELDAS Y SENTIDO NO ESTA TERMINADO DE DEFINIR PERO ES UNA RESPONSABILIDAD COMPARTIDA ENTRE EL OBJ TABLERO Y EL OBJ PALABRA PARA QUE LOS MOVIMIENTOS DE LA IA TRABAJE USANDO TABLERO Y PALABRA.
            self.set_sentido_horizontal(True)          # sentido horizontal
        else:
            self.set_sentido_horizontal(False)         # sentido vertical

    def validar_lugar(self, pos):
        if self.get_sentido_horizontal = True:
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
            self.set_sentido_horizontal(None)                              # pone el sentido en none en caso de borrar y cambiar el sentido de la palabra
        elif self.cant_letras() == 1 and validar_lugar(pos):    # si hay una entra y valida el sentido
            self.validar_sentido(pos)
            self.agregar_letra_final(letra)
            self.agregar_coord_final(tupla)
            self.sumar_puntos()
