from celda import Celda

class Tablero(): # tablero es un objeto donde se guardan objetos celdes y sus metodos realizan las operaciones logicas de procesar la informacion
    def __init__(self, ejes = 15):
        self.matriz = [[None] * ejes for i in range(ejes)] # carga el tablero vacio ---> None
        for x in range(len(tablero)):
            for y in range(len(tablero[x])):
                self.matriz[x][y] = Celda()       # pisa el objeto None con un objeto celda, cada celda esta vacia
    #getter y setter
    def get_letra(self, x, y):
        return matriz[x][y].get_letra()

    def set_letra(self, x , y, letra):
        matriz[x][y].set_letra(letra)

    def get_modificador(self, x, y):
        return matriz[x][y].get_modificador()

    def set_modificador(self, x , y, modificador):
        matriz[x][y].set_modificador(modificador)

    def ultima_letra(self):
        return

    def set_letra(self, x , y, letra):
        matriz[x][y].set_letra(letra)

#####################################################################################
import PySimpleGUI as sg
import funciones as f

bolsa_letras = f.bolsa_de_letras

bolsa_jugador = []

bolsa_maquina = []

f.crear_bolsas(bolsa_letras,bolsa_jugador,bolsa_maquina)


def pintarTablero(matriz,g):
    #ACA DIBUJAMOS EL TABLERO
    rango=15
    for row in range(rango):
            for col in range(rango):
                #EN ESTA PARTE HACEMOS LAS DIVISIONES DE LAS CELDAS CON UNA LINEA BLANCA
                matriz[row][col]=g.DrawRectangle((col * tam_celda + 5, row * tam_celda + 3),
                                                (col * tam_celda + tam_celda + 5, row * tam_celda + tam_celda + 3),
                                                line_color='white')
                #ACA PINTAMOS LAS CELDAS COLOR DORADO
                if (row==0 or row==7 or row==14)and(col==0 or col==7 or col==14):
                        matriz[row][col]=g.DrawRectangle((col * tam_celda + 5, row * tam_celda + 3),
                                                        (col * tam_celda + tam_celda + 5, row * tam_celda + tam_celda + 3),
                                                        fill_color='goldenrod',line_color='white')
                #ACA PINTAMOS LAS CELDAS COLOR CELESTE
                if ((row==1 or row==13)and(col==5 or col==9))or((row==5 or row==9)and(col==1 or col==13))or ((row==6 or row==8) and (col==6 or col==8)):
                        matriz[row][col]=g.DrawRectangle((col * tam_celda + 5, row * tam_celda + 3),
                                                        (col * tam_celda + tam_celda + 5, row * tam_celda + tam_celda + 3),
                                                        fill_color='skyblue',line_color='white')
                #ACA PINTAMOS LAS CELDAS COLOR VERDE
                if ((row==0 or row==14 or row==7)and(col==3 or col==11))or((row==3 or row==11)and(col==0 or col==14 or col==7))or((row==6 or row==8) and (col==2 or col==12))or((row==2 or row==12) and (col==6 or col==8)):
                        matriz[row][col]=g.DrawRectangle((col * tam_celda + 5, row * tam_celda + 3),
                                                        (col * tam_celda + tam_celda + 5, row * tam_celda + tam_celda + 3),
                                                        fill_color='mediumseagreen',line_color='white')
                #ACA PINTAMOS LAS CELDAS COLOR ROJO
                if (row in range (1,6))or(row in range(9,14)):
                    if (row==col):
                        matriz[row][col]=g.DrawRectangle((col * tam_celda + 5, row * tam_celda + 3),
                                                        (col * tam_celda + tam_celda + 5, row * tam_celda + tam_celda + 3),
                                                         fill_color='indianred',line_color='white')
                        matriz[row][((rango-1)-row)]=g.DrawRectangle((((rango-1)-row) * tam_celda + 5, row * tam_celda + 3),
                                                        (((rango-1)-row) * tam_celda + tam_celda + 5, row * tam_celda + tam_celda + 3),
                                                        fill_color='indianred',line_color='white')


tam_celda =15

#un lambda robado que crea botones del nombre que le llega como parametro
button = lambda name : sg.Button(name,key = name)

layout = [
         [sg.T(' ' * 5)],
         [sg.Graph((500,500),(0,232),(235,0), key='_GRAPH_', background_color='gainsboro',change_submits=True, drag_submits=False)],
         [sg.Text("Tus Fichas: ")],[button(i) for i in bolsa_jugador],
         [sg.Text("FICHAS DE LA MAQUINA: ")],[button(i) for i in bolsa_maquina],
         [sg.Button("Evaluar"),sg.Button("Cancelar"),sg.Button("borrar")]                   ]

window = sg.Window('Ejercicio1', ).Layout(layout).Finalize()
g = window.FindElement('_GRAPH_')

matriz=[]

#son las casillas ocupadas,deberia usarse antes de escribir
elegido=[]

#en texto se guardan las letras que voy eligiendo
texto=[]

for i in range(0,15):
    matriz.append([0]*15)
    elegido.append([False]*15)
    texto.append([""]*15)
#ACA DIBUJAMOS EL TABLERO
pintarTablero(matriz,g)

#cancelados es para poder crear una lista de fichas para hacer un rollback
cancelados = []

#marque es un boolean que me permite escribir en el tablero solo cuando se activa,se deberia activar si el evento es alguno de los botones
marque_una_letra = False

while True:
    f = matriz
    f2 = g
    event, values = window.Read()
    print(event)
    print(values)
    if event is None or 'tipo' == 'Exit':
        break
    #si el evento es graph deberia ser una casilla del tablero
    if event == '_GRAPH_':
        if values['_GRAPH_'] == (None,None):
            continue
        mouse = values["_GRAPH_"]
        box_x = mouse[0]//tam_celda
        box_y = mouse[1]//tam_celda
        print(box_x,box_y)
    #sino el evento puede ser algun boton de las letras del jugador
    elif event in bolsa_jugador:
        #guardo el evento como letra,nose bien xq hice esto
        letra = event
        #solo puede escribir en el tablero cuando cambie marcado
        marque_una_letra = True
        if marque_una_letra:
            #en la coordenada x,y dibujo la letra
            texto[box_x][box_y] = g.DrawText(letra, (box_x * tam_celda + 13, box_y * tam_celda + 10))
            print(bolsa_jugador)
            print(letra)
            #guardo las fichas que fui usando
            cancelados.append(letra)
            #borro de la bolsa del jugador la que use
            bolsa_jugador.remove(letra)
            print(bolsa_jugador)
            #cambio la visibilidad del boton para simular que la use
            window.Element(letra).Update(visible=False)
            #lo devuelvo a false para que no siga escribieno
            marque_una_letra = False
    #pensaba borrar la ultima letra pero nose como
    elif event == "borrar":
        texto[box_x][box_y] = g.DrawText("esto esta borrado", (box_x * tam_celda + 13, box_y * tam_celda + 10))
    #cancelar deberia reccorrer una lista con las letras que puse y devolver su correspondiente boton a visible
    elif event=="Cancelar":
        for letra in cancelados:
            window.Element(letra).Update(visible=True)
        #matriz = f queria volver el tablero a vacio pero nose como
