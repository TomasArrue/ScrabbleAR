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
color_button = ('black','white')# color de los botones
tam_button = 1,1 #tamanio de los botones
button = lambda name : sg.Button(name,button_color=color_button,size=tam_button) #seteo del boton


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
    matriz.append([0]*15)#cargamos la matriz con los valores de la celda
    elegido.append([False]*15)#cargamos la matriz elegido con false que es el esado inicial de las celdas, todas libres
    texto.append([""]*15)#cargamos la matriz con espacios vacios, donde luego iran letras
#ACA DIBUJAMOS EL TABLERO
pintarTablero(matriz,g)

#cancelados es para poder crear una lista de fichas para hacer un rollback
cancelados = []

#marque es un boolean que me permite escribir en el tablero solo cuando se activa,se deberia activar si el evento es alguno de los botones
marque_una_letra = False

#al seleccionar una celda se pone de color verde
Check_box = lambda x,y : g.TKCanvas.itemconfig(matriz[box_y][box_x], fill="grey")
#al seleccionar un boton se pinta de color azul
Check_button = lambda x: window.FindElement(x).Update(button_color=('white','blue'))
Uncheck_button = lambda x: window.FindElement(x).Update(button_color=('black','white'))
current_Check_button = ''

button_selected=False
letra= '' #Se ira guardando la letra que se coloca en las celdas
word='' # palabra que se va formando con las letras
palabraCargada=[]#para cargar la palabra que vamos cargando y verificar si es horizontal o vertical
while True:
    f = matriz
    f2 = g
    event, values = window.Read()
    print(event)
    print(values)
    if event is None or 'tipo' == 'Exit':
        break
    
    '''
    #sino el evento puede ser algun boton de las letras del jugador
    if event in bolsa_jugador:
        #guardo el evento como letra,nose bien xq hice esto
        letra = event
        #solo puede escribir en el tablero cuando cambie marcado
        marque_una_letra = True
        if marque_una_letra:
            '''
    
    if event == '_GRAPH_':
        if values['_GRAPH_'] == (None,None):
            continue
        mouse = values["_GRAPH_"]
        box_x = mouse[0]//tam_celda
        box_y = mouse[1]//tam_celda
        print(box_x,box_y)
        if mouse == (None, None) or box_x >14  or box_y > 14:
            continue
        if button_selected: # si hay un boton seleccionado
            
            print('ds')
            #Si esta libre la Celda se escribe
            print(elegido[box_x][box_y])
            print(texto[box_x][box_y])
            if elegido[box_x][box_y]==False and texto[box_x][box_y]=="":
                print(letra)
                #chequeamos la orientacion de la palabra 
                palabraCargada.append(letra)
            
                if len(palabraCargada)==1: #vemos si es la primera letra, seteamos la orientacion de la palabra
                    #print('es la primiera letra')
                    vertical=False
                    horizontal=False
                    #Check_box(box_x,box_y)
                    texto[box_x][box_y] = g.DrawText(letra, (box_x * tam_celda + 13, box_y * tam_celda + 10))
                    elegido[box_x][box_y]=True
                    box_X_horizontal=box_x#esta variable sirve para guardar la cord X horizontal anterior
                    box_Y_horizontal=box_y#esta variable sirve para guardar la cord Y horizontal anterior
                    box_X_vertical=box_x#esta variable sirve para guardar la cord X vertical anterior
                    box_Y_vertical=box_y#esta variable sirve para guardar la cord Y vertical anterior
                    Uncheck_button(letra) # deseleccionamos el boton
                    button_selected = False # lo marcamos en Falso, porque NO esta seleccionado
                    window.Element(letra).Update(visible=False) #oculta el boton con la letra usada
                    
                if len(palabraCargada)==2: #vemos la segunda letra, dependiendo donde este sabremos la orientacion de la palabra
                    #print ('es la segunda letra')
                    #print(box_x ,'y', box_X_horizontal+1)
                    if box_X_horizontal+1==box_x and box_Y_horizontal==box_y:
                        print('es horizontal')  
                        horizontal=True 
                        Check_box(box_x,box_y)#al colocar la letra en el tablero , la casilla se pinta de gris
                        texto[box_x][box_y] = g.DrawText(letra, (box_x * tam_celda + 13, box_y * tam_celda + 10))
                        elegido[box_x][box_y]=True
                        box_X_horizontal=box_x
                        box_Y_horizontal=box_y
                        Uncheck_button(letra)
                        button_selected = False 
                        window.Element(letra).Update(visible=False)
                    else:
                        if box_X_vertical==box_x and box_Y_vertical+1==box_y:
                            print('es vertical')  
                            vertical=True 
                            Check_box(box_x,box_y)#al colocar la letra en el tablero , la casilla se pinta de gris
                            texto[box_x][box_y] = g.DrawText(letra, (box_x * tam_celda + 13, box_y * tam_celda + 10))
                            elegido[box_x][box_y]=True
                            box_X_vertical=box_x
                            box_Y_vertical=box_y
                            Uncheck_button(letra)
                            button_selected = False 
                            window.Element(letra).Update(visible=False)
                    
                if vertical:
                    print('es verti')  
                    print( box_Y_vertical+1 ,' y ',box_y)
                    if box_X_vertical==box_x and box_Y_vertical+1==box_y:
                        Check_box(box_x,box_y)#al colocar la letra en el tablero , la casilla se pinta de gris
                        texto[box_x][box_y] = g.DrawText(letra, (box_x * tam_celda + 13, box_y * tam_celda + 10))
                        elegido[box_x][box_y]=True
                        box_X_vertical=box_x
                        box_Y_vertical=box_y
                        Uncheck_button(letra)
                        button_selected = False 
                        window.Element(letra).Update(visible=False)

                if horizontal:
                    print('es hori') 
                    print( box_X_horizontal+1 ,' y ',box_x)
                    if box_X_horizontal+1==box_x and box_Y_horizontal==box_y:
                        print( box_X_horizontal+1 ,' y ',box_x)
                        print(letra)
                        Check_box(box_x,box_y)#al colocar la letra en el tablero , la casilla se pinta de gris
                        texto[box_x][box_y] = g.DrawText(letra, (box_x * tam_celda + 13, box_y * tam_celda + 10))    
                        elegido[box_x][box_y]=True
                        box_X_horizontal=box_x
                        box_Y_horizontal=box_y
                        Uncheck_button(letra)
                        button_selected = False 
                        window.Element(letra).Update(visible=False)
                
                #en la coordenada x,y dibujo la letra
                
                print(bolsa_jugador)
                print(letra)


        
                #guardo las fichas que fui usando
                cancelados.append(letra)
                #borro de la bolsa del jugador la que use
                #bolsa_jugador.remove(letra)    
                #print(bolsa_jugador)
                #cambio la visibilidad del boton para simular que la use
           
                #lo devuelvo a false para que no siga escribieno
                marque_una_letra = False
    else:
        #aca es para la seleccion de la las fichas
        if button_selected: #si el boton esta seleccionado
            if event == letra:
                Uncheck_button(event) # deseleccionamos el boton
                button_selected = False # lo marcamos en Falso, porque NO esta seleccionado
                letra = ''
        else:
            Check_button(event) #seleccionamos el boton sino esta seleccionado
            button_selected = True # lo marcamos en True, porque SI esta seleccionado
            letra = event #se guarda la letra correspondiente a la ficha   

    #pensaba borrar la ultima letra pero nose como
    if event == "borrar":
        texto[box_x][box_y] = g.DrawText("esto esta borrado", (box_x * tam_celda + 13, box_y * tam_celda + 10))
    #cancelar deberia reccorrer una lista con las letras que puse y devolver su correspondiente boton a visible
    if event=="Cancelar":
        for letra in cancelados:
            window.Element(letra).Update(visible=True)
        #matriz = f queria volver el tablero a vacio pero nose como
