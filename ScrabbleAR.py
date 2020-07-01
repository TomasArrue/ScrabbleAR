import sys  # usamos el import sys para abortar el programa en caso de que los archivos no esten disponibles para ejecutar
import json
import PySimpleGUI as sg
import random
from string import ascii_uppercase as up
from random import choice
from pattern.text.es import lexicon,spelling,verbs


def configuracion_de_juego():
    """
        configuracion del juego inicial,cargamos el config.json, para poder cambiar
        la cantidades de letras iniciales en la bolsa de fichas y ademas podemos
        editar el valor de cada ficha
    """
    with open('config.json','r') as cf:
        c = json.load(cf)

    diccionario_cantidad_de_letras=c['cantidad_de_letras']
    diccionario_cantidad_de_puntos=c['valor_por_letra']

    layout3=[
                [sg.Text("Configuracion", size=(10, 1), justification='left', font=("Chalkboard", 25), relief=sg.RELIEF_RIDGE)],
                [sg.Text(k,size=(3,1),justification='center')for k,v in diccionario_cantidad_de_letras.items()],
                [sg.Text('PARA MODIFICAR LA CANTIDAD DE LETRAS POR LETRA CAMBIE EL VALOR A LA LETRA CORRESPONDIENTE :')],
                [sg.Input(v,size=(3,1),key=(k+'_cant'))for k,v in diccionario_cantidad_de_letras.items()],
                [sg.Text('PARA MODIFICAR EL VALOR DE LAS LETRAS POR LETRA CAMBIE EL VALOR A LA LETRA CORRESPONDIENTE:')],
                [sg.Input(v,size=(3,1),key=(k+'_valor'))for k,v in diccionario_cantidad_de_puntos.items()],
                [sg.Text('')],
                [sg.Text('PARA MODIFICAR EL TIEMPO INGRESE EL TIEMPO EN MINUTOS (de 5 a 30) QUE QUIERES QUE DURE LA PARTIDA')],
                [sg.Input(size=(9,1),key=('time'))],
                [sg.Button('GUARDAR CONFIGURACION'),sg.Button('CANCELAR')]
            ]

    window3 = sg.Window('Configuracion').Layout(layout3)
    while True:
        event3, values3 = window3.Read()

        if event3 == 'CANCELAR':
            break

        if event3 == 'GUARDAR CONFIGURACION':
            # with open('config.json','w') as cf:

            try:
                num_tiempo=int(values3['time'])
                if ( num_tiempo > 30 ):
                    num_tiempo=30
                if ( num_tiempo < 5 ):
                    num_tiempo=5
            except (ValueError):
                    num_tiempo= 15 # seteamos 15 minutos en caso de cargar erronea, pero informamos que se cargo mal el tiempo
                    sg.Popup('El tiempo se cargo de maneara erronea, pero cargamos la partida de 15 minutos')

            for k,v in diccionario_cantidad_de_letras.items():
                # print('valores: ',values3[k+'_cant'])
                # print (type(values3[k+'_cant']))
                try:
                    numero_nuevo=int(values3[k+'_cant'])
                except (ValueError):
                    numero_nuevo=1
                print(numero_nuevo)
            sg.Popup('La duracion de la partida sera de: ',num_tiempo,' minutos')



    window3.close()


def crear_bolsita_total():
    """
        Generamos la bolsas con las fichas totales para usar en el juego,
        las cuales tenemos almacenadas en el config.json
    """
    with open('config.json','r') as cf:
        c = json.load(cf)
    bolsa = c['cantidad_de_letras']
    return bolsa


def crear_atril(bolsa_total):
    """
        Toma las letras de a una desde el archivo configuracion
    """
    letra = random.choice(list(bolsa_total.keys()))
    while bolsa_total[letra] == 0:
            letra= random.choice(list(bolsa_total.keys()))
    bolsa_total[letra] -= 1

    return letra


def carga_nombre():
    """
        Cargamos el nombre al ingresar al juego para usarlo luego al cargar los
        datos de la partida, tambien lo utilizamos para que indique el puntaje
        del jugardor activo en el momento
    """
    layout3=[[sg.Text('Ingresa tu nombre:')],
            [sg.Input('',key='name')],
            [sg.Button('Listo')]]
    window3=sg.Window('Ingresa datos',layout3)
    while True:
         event,values=window3.read()
         if event=='Listo' :
             nombre=values['name']
             break
    window3.close()
    return nombre


def asignar_colores_al_tablero(window,dificultad):
    """
       Se van a pintar los botones de la matriz que conforman el tablero
       segun las coordenas que vengan en el archivo json, dependiendo
       el nivel que hayamos elegido
    """
    with open('config.json','r') as t:
        dic = json.load(t)

    print(dificultad)
    tablero_config = dic[dificultad]

    for colores in tablero_config.keys():
        lista_de_cord = tablero_config[colores]
        for par_de_cord in lista_de_cord:
            x,y = par_de_cord
            window[x,y].update(button_color=(colores,colores))


def cargar_juego(window,timer_running,nombre,bolsa_total):
    """
        iniciamos todo el seteo inicial del juego:
            -la dificultad segun la seleccionada en el menu
            -Pintamos el tablero segun la dificultad
            -Ocultamos los botones de Comenzar, Cargar Partida
            -Volvemos visibles los botones de Guardar, Salir
            -Volvemos visibles las opciones de juego para poder jugar
    """
    very_dificult=values['dificultad']
    asignar_colores_al_tablero(window,very_dificult)
    window['opcionesJuego'].update(visible=True)
    window['Comenzar'].update(visible=False)
    window['Configuracion'].update(visible=False)
    window['Cargar Partida'].update(visible=False)
    window['Guardar Partida'].update(visible=True)
    window['Salir'].update(visible=True)
    window['puntaje_propio'].update("PUNTAJE DE {0} ES :0".format(nombre))
    window['puntaje'].update(visible=True)
    window['atrilFichasRival'].update(visible=True)
    window['atrilFichas'].update(visible=True)
    window['dificultad'].update(visible=False)
    for i in range(7):# carga de las 7 fichas al inicio

        nro_de_boton='Boton_'+str(i+1)
        obtener_fichas(window,nro_de_boton,a,bolsa_total)

    timer_running = not timer_running

    return timer_running, very_dificult


def volver_a_pintar_la_casilla(cord,window):
    """
        este modulo nos sirve para volver a pintar un boton de su color inicial
        en caso de que tengamos que sacar una ficha que pusimos
    """
    with open ('config.json','r') as p:
        dicc = json.load(p)
    # la dific tiene que vernir como parametro para saber que tablero abrir
    tablero_actual = dicc["Facil"]
    if list(cord) in tablero_actual["indianred"]: window[cord].update(button_color=('indianred','indianred'))
    elif list(cord) in tablero_actual["goldenrod"]: window[cord].update(button_color=('goldenrod','goldenrod'))
    elif list(cord) in tablero_actual["mediumseagreen"]: window[cord].update(button_color=('mediumseagreen','mediumseagreen'))
    elif list(cord) in tablero_actual["skyblue"]: window[cord].update(button_color=('skyblue','skyblue'))
    # elif list(cord) in tablero_actual["grey"]: window[cord].update(button_color=('grey','grey'))
    else: window[cord].update(button_color=('grey','white'))


def verificar_palabra(palabra):
    """
        verificamos si la palabra es valida
    """
    if palabra in lexicon and spelling or palabra in verbs:
        return(True)
    else:
        return(True) #cambiar a false


def obtener_fichas(window,nro_de_boton,a,bolsa_total):
    """
        Este metodo nos da una ficha "nueva".
        Generamos una letra random la agregamos a la lista de letras de nuestro atril,
        luego con la key del boton recibida como parametro actualizamos el valor del
        boton con la nueva letra
    """
    letra=crear_atril(bolsa_total)
    a.append(letra)
    window[nro_de_boton].update(letra)
    window[nro_de_boton].update(button_color=('black','oldlace'))
    window.Refresh()


def repartir_fichas_de_nuevo(window,cantidad_de_veces_Repartidas,a):
    """
        Utilizamos este metodo para poder cambiar la mano de fichas que tenemos,
        y tenemos permitido hacerlo hasta 3 veces
    """
    a=[]
    if (cantidad_de_veces_Repartidas < 3):
        cantidad_de_veces_Repartidas=cantidad_de_veces_Repartidas+1
        for i in range(7):#carga de las 7 fichas
            nro_de_boton='Boton_'+str(i+1)
            obtener_fichas(window,nro_de_boton,a,bolsa_total)
    else:
        sg.Popup('Ya hiciste el maximo de cambios de mano')
    return cantidad_de_veces_Repartidas


def quitar_fichas(window,usados:list,botones_usados:list,no_disponibles:list):
    """
        quitar fichas nos permite sacar las fichas ingresadas al tablero en el turno correspondiente.
        Mientras que la longitud lista de usados del turno sea mayor a 0 vamos a poder retirar fichas
        que ingresamos, en caso de que no se pueda no podremos quitar mas
    """
    # print(len(usados),' ',len(no_disponibles),' ',len(botones_usados))
    if len(usados)>0:                                  # Aca antes de borrar una letra vamos a preguntar si hay letras para borrar, en caso contrario no podras borrar mas letras
        letra_a_borrar = usados.pop(len(usados) - 1)   # Saca la ultima letra de la palabra cargada - el pop saca de usados  el elemento de la ultima posicion de la lista de usados
        boton_a_recuperar = botones_usados.pop(len(botones_usados)-1)
        a.append(letra_a_borrar)                       # vuelve a cargar la letra que sacamos del tablero en el atril de nuestras fichas
        coord_a_liberar = no_disponibles.pop(len(no_disponibles) - 1) # Saca la ultima coordenada de la palabra cargada - el pop saca de no_disponibles el elemento de la ultima posicion de la lista de no_disponibles
        volver_a_pintar_la_casilla(coord_a_liberar,window) # vuelve a pintar la casilla de su color en estado inicial
        window[coord_a_liberar].update("")
        window[boton_a_recuperar].update(button_color=('black','oldlace'),disabled=False)
    else:
        sg.Popup('No hay fichas para borrar')


def pedir_fichas(window,botones_usados,a,bolsa_total):
    """
       El pedir fichas nos permite pedir la cantidad de fichas usadas en el ultimo turno
       hasta llegar a tener 7 nuevamente.
    """
    for i in botones_usados:
        letra=a[len(a)-1]
        window[i].update(letra,disabled = False)
        obtener_fichas(window,i,a,bolsa_total)
    for i in range (len(botones_usados)):
        botones_usados.pop()


def letra_al_tablero(window,usados,botones_usados,a,no_disponibles):
    """
       Utilizamos este metodo para graficar el colocar la ficha en el tablero.
       -Guardamos la ficha en una lista de "usados"
       -Guardamos el nombre del boton para luego recuperarlo
       -En el tablero ponemos el valor de la ficha seleccionada
       -Sacamos la letra de nuestro atril, y la deshabilitamos del atril
       -Para finalizar guardamos las coordenadas del lugar en una lista de lugares no disponibles
    """
    usados.append(letra)
    botones_usados.append(event)
    window[lugar].update(letra, button_color=('black','oldlace'))
    a.remove(letra)
    window[event].update(button_color=('darkgrey','darkgrey'),disabled = True)
    no_disponibles.append(lugar)


def puntos_de_letra(letra,dificultad,coord):
    """
       calculamos el valor de la letra ingresada en el tablero. accedemos al json para ver su puntaje asociado
    """
    with open ('config.json','r') as p:
        dicc = json.load(p)
    valor_de_letra = dicc["valor_por_letra"]
    tablero_actual = dicc[dificultad]

    # lo tengo que castear a lista porque asi quedo grabado en el json
    if list(coord) in tablero_actual["indianred"]:
        v = valor_de_letra[letra]+5
        return v
    elif list(coord) in tablero_actual["goldenrod"]:
        f = valor_de_letra[letra]*2
        return f
    elif list(coord) in tablero_actual["mediumseagreen"] or list(coord) in tablero_actual["skyblue"]:
        return valor_de_letra[letra]
    else:
        return valor_de_letra[letra]


def puntos_de_palabra(dificultad,no_disponibles,puntos):
    """
       En esta parte vamos a calcular el total de los puntos de la palabra cargada.
       Segun la dificultad vamos a tener distintos modificadores en cada color
       Si nuestra palabra pasa por casillas con colores el puntaje final se vera afectado
    """
    with open ('config.json','r') as p:
        dicc = json.load(p)
    tablero_actual = dicc[dificultad]
    # conjuntos para hacer la interseccion
    green = set(map(tuple,tablero_actual["mediumseagreen"]))
    blue = set(map(tuple,tablero_actual["skyblue"]))
    int_green = green.intersection(set(no_disponibles))
    #print(int_green)
    #print(type(green))
    #print(green,'conjunto verde')
    int_blue = blue.intersection(set(no_disponibles))
    for element in int_green:
        puntos = puntos * 3
    for element in int_blue:
        puntos = puntos + puntos/2
    return puntos
    # print(blue,'conjunto celeste')

###### INICIA EL PROGRAMA PRINCIPAL ############################################

try:
    with open('config.json','r') as cf:
        pass
except FileNotFoundError:
    sg.Popup('ERROR ---> config.json NO ENCONTRADO')
    sys.exit()

bolsa_total = crear_bolsita_total()

atril_maquina = crear_atril(bolsa_total)

color_De_Boton=('Black','seagreen')
tamanio_Boton_De_Fichas = 2,2 # tamanio de botones que seran las fichas
tamanio_Boton_De_Control = 15,1 # tamanio de botones de comenzar y salir
max_Cant_Filas = max_Cant_Columnas = 15 # tamanio de las matrices
dificultad = ['Facil','Medio','Dificil'] # combobox
botones_De_Fichas = lambda name : sg.Button(name,button_color=color_De_Boton,size=tamanio_Boton_De_Fichas)
botones_De_Fichas_rival = lambda name : sg.Button('?',button_color=color_De_Boton,size=tamanio_Boton_De_Fichas)
sg.ChangeLookAndFeel('DarkGrey6') #thema del PySimpleGUI

#VENTANA PRINCIPAL
opciones_de_inicio = [ [sg.Button("Comenzar",size=tamanio_Boton_De_Control)],
                       [sg.Button("Cargar Partida",size=tamanio_Boton_De_Control)],
                       [sg.Button('Configuracion',size=tamanio_Boton_De_Control)],
                       [sg.InputCombo(dificultad,default_value='Facil', size=(10, 10),key='dificultad')],
                       [sg.Button('Guardar Partida',size=tamanio_Boton_De_Control,visible=False)],
                       [sg.Button('Salir',size=tamanio_Boton_De_Control)]
                     ]

# VENTANA DEL JUEGO
opciones_de_juego = [ [sg.Button('Borrar',size=tamanio_Boton_De_Control),
                      sg.Button("Evaluar",size=tamanio_Boton_De_Control),
                      sg.Button("Repartir De Nuevo",size=tamanio_Boton_De_Control),
                      sg.Button("TOP",size=tamanio_Boton_De_Control)]
                    ]
#FICHAS DEL JUGADOR
fichas=[ [sg.Text("Tus Fichas: ",font=("Chalkboard", 15))],
         [sg.Button('',button_color=('black','oldlace'),size=(tamanio_Boton_De_Fichas),key="Boton_1",pad=(5,5)),
          sg.Button('',button_color=('black','oldlace'),size=(tamanio_Boton_De_Fichas),key="Boton_2",pad=(5,5)),
          sg.Button('',button_color=('black','oldlace'),size=(tamanio_Boton_De_Fichas),key="Boton_3",pad=(5,5)),
          sg.Button('',button_color=('black','oldlace'),size=(tamanio_Boton_De_Fichas),key="Boton_4",pad=(5,5)),
          sg.Button('',button_color=('black','oldlace'),size=(tamanio_Boton_De_Fichas),key="Boton_5",pad=(5,5)),
          sg.Button('',button_color=('black','oldlace'),size=(tamanio_Boton_De_Fichas),key="Boton_6",pad=(5,5)),
          sg.Button('',button_color=('black','oldlace'),size=(tamanio_Boton_De_Fichas),key="Boton_7",pad=(5,5))
         ]]

#FICHAS DEL NPC
fichas_rival =[ [sg.Text("Fichas CPU: ",font=("Chalkboard", 15))],
                [botones_De_Fichas_rival(j) for j in atril_maquina]
              ]

tablero=[ [sg.Button('',button_color=('grey','white'),size=(1, 1), key=(i,j), pad=(0,0)) for j in range(max_Cant_Columnas)] for i in range(max_Cant_Filas)]#botones matriz

puntaje_y_tiempo=[[sg.Text('TU PUNTAJE:',font=("Chalkboard", 10))],[sg.Text('00',key='puntaje_propio',font=("Chalkboard", 10))],
                   [sg.Text('PUNTAJE PC: 0',font=("Chalkboard", 10))],
                   [sg.Text('Tiempo',font=('Chalkboard', 15))],
                   [sg.Text('00:00',font=('Chalkboard', 15), key='-OUTPUT-')],#
                   [sg.T(' ' * 5)]
                 ]

layout=[
       [sg.Text("Scrabble", size=(8, 1), justification='left', font=("Chalkboard", 25), relief=sg.RELIEF_RIDGE)],
       [sg.Column(fichas_rival,key='atrilFichasRival',justification='center',visible=False)],
       [sg.Column(opciones_de_inicio,key='opcionesComienzo',justification='left'), sg.Column(tablero),sg.Column(puntaje_y_tiempo,key='puntaje',visible=False)],
       [sg.Column(fichas,key='atrilFichas',justification='center',visible=False)],
       [sg.Column(opciones_de_juego,key='opcionesJuego',justification='center',visible=False)],
       ]

window = sg.Window('SCRABBLE', layout, default_button_element_size=(2,2),finalize=True, resizable=True,  auto_size_buttons=True)

puntos = 0          # puntos del jugdador,(en realidad hay que tener 2)
a=[]                # letras que voy usando
usados = []         # lleva las letras que ya use
botones_usados=[]   # nombre de los botones que voy usando
no_disponibles = [] # lleva la cuenta de los lugares que ya escribi
ant = ()            # para despintar la casilla anterior cuando toco una nueva
lugar = ()          # marca la casilla actual
layout2 = layout    # esto no se que es
cantidad_de_veces_Repartidas = 0 # cantidad de veces de pedidos para hacer el cambio de fichas totales
timer_running, counter = False, 0 # seteos para el timer,
dificult=''         # la dificultad actual que luego sera asignada

while True:
    event, values = window.read(timeout=10)
    if event in (None, 'Salir'):
        break
    else:
         if type(event) is tuple:
             lugar = event
             if lugar not in no_disponibles: # pinto el lugar que estoy seleccionando,hago esa pregunta para que no trate de marcar un casillero que ya tiene una letra
                 window[lugar].update(button_color=('white','darkgrey'))
             if (ant) and (ant not in no_disponibles): # digo que si anterior tiene algo que despinte lo anterior
                 volver_a_pintar_la_casilla(lugar,window)
             ant = lugar,

         if event in  ("Boton_1","Boton_2","Boton_3","Boton_4","Boton_5","Boton_6","Boton_7") and lugar:#si el evento seria una letra y lugar tiene algo es xq marque algo del tabler
                 letra = window[event].GetText() # asigno la letra del evento

                 if lugar not in no_disponibles: # si el lugar no lo use
                     if len(usados) == 0:        # vemos si es la primera letra, seteamos la orientacion de la palabra
                        letra_al_tablero(window,usados,botones_usados,a,no_disponibles)
                        #print(dificult)
                        puntos += puntos_de_letra(letra,dificult,lugar) # hay que declarar una variable dific para enviar en lugar de facil
                        #print(puntos)
                        window["puntaje_propio"].update(puntos)
                        vertical=horizontal=False
                        box_X_vertical=box_X_horizontal=lugar[1]  # estas variables sirven para guardar la cord X horizontal y vertical anterior
                        box_Y_vertical=box_Y_horizontal=lugar[0]  # estas variables sirven para guardar la cord Y horizontal y vertical anterior
                     elif len(usados)==1: # vemos si es la primera letra, seteamos la orientacion de la palabra
                         if box_X_horizontal+1==lugar[1] and box_Y_horizontal==lugar[0]:
                            horizontal=True
                            letra_al_tablero(window,usados,botones_usados,a,no_disponibles)
                            puntos += puntos_de_letra(letra,dificult,lugar)
                            #print(puntos)
                            window["puntaje_propio"].update(puntos)
                            box_X_horizontal=lugar[1]
                            box_Y_horizontal=lugar[0]
                         elif box_X_vertical==lugar[1] and box_Y_vertical+1==lugar[0]:
                            vertical=True
                            letra_al_tablero(window,usados,botones_usados,a,no_disponibles)
                            puntos += puntos_de_letra(letra,dificult,lugar)
                            print(puntos)
                            window["puntaje_propio"].update(puntos)
                            box_X_vertical=lugar[1]
                            box_Y_vertical=lugar[0]
                     elif len(usados)>1:
                         if vertical:
                                if box_X_vertical==lugar[1] and box_Y_vertical+1==lugar[0]:
                                    letra_al_tablero(window,usados,botones_usados,a,no_disponibles)
                                    puntos += puntos_de_letra(letra,dificult,lugar)
                                    #print(puntos)
                                    window["puntaje_propio"].update(puntos)
                                    box_X_vertical=lugar[1]
                                    box_Y_vertical=lugar[0]
                                else:
                                    sg.Popup('Lugar Invalido')
                         elif horizontal:
                                if box_X_horizontal+1==lugar[1] and box_Y_horizontal==lugar[0]:
                                    letra_al_tablero(window,usados,botones_usados,a,no_disponibles)
                                    puntos += puntos_de_letra(letra,dificult,lugar)
                                    #print(puntos)
                                    window["puntaje_propio"].update(puntos)
                                    box_X_horizontal=lugar[1]
                                    box_Y_horizontal=lugar[0]
                                else:
                                    sg.Popup('Lugar Invalido')

         elif event == "Repartir De Nuevo": # pide 7 fichas nuevas en la mano
             if not botones_usados:
                cantidad_de_veces_Repartidas=repartir_fichas_de_nuevo(window,cantidad_de_veces_Repartidas,a)
             else:
                sg.Popup('Estas en medio de una mano, tenes q tener 7 fichas para cambiar')

         elif event == "Borrar" : #quita elementos del tablero, desde el ultimo al primero
            puntos -= puntos_de_letra(usados[len(usados)-1],dificult,no_disponibles[len(no_disponibles)-1])
            window["puntaje_propio"].update(puntos)
            quitar_fichas(window,usados,botones_usados,no_disponibles)

         elif event == "Comenzar": # para inicializar el juego
             nombre=carga_nombre()
             timer_running, dificult = cargar_juego(window,timer_running,nombre,bolsa_total)

         elif event == "Configuracion":
             configuracion_de_juego()

         elif event == "TOP":
            with open ('ranking.json','r') as r:
                dicc = json.load(r)

            #print(dicc.keys())
            #print(dicc.values())

            rank_facil = list(dicc['facil'].items())
            #print('valores en facil',rank_facil)

            rank_medio = list(dicc['medio'].items())
            #print('valores en medio',rank_medio)

            rank_dif = list(dicc['dificil'].items())
            #print('valores en dificil',rank_dif)

            tab1_layout = [[sg.T('This is inside tab 1')]]
            tab2_layout = [[sg.Listbox(values=rank_facil, size=(30,10))]]
            tab3_layout = [[sg.Listbox(values=rank_medio, size=(30,10))]]
            tab4_layout = [[sg.Listbox(values=rank_dif, size=(30,10))]]
            layout2 = [
                        [sg.Text('RANKING'), sg.Text('', key='_OUTPUT_')],
                        [sg.TabGroup([

                                        [sg.Tab('Ranking General', tab1_layout, tooltip='tip'),
                                         sg.Tab('Ranking Facil', tab2_layout, tooltip='tip2'),
                                         sg.Tab('Ranking Medio', tab3_layout, tooltip='tip3'),
                                         sg.Tab('Ranking Dificil', tab4_layout,tooltip='tip4')]

                                    ])],
                        [sg.Button('Exit')]
                      ]
            window2 = sg.Window('TOP TEN').Layout(layout2)
            while True:
                event2, values2 = window2.Read()
                if event2 == 'Exit':
                    break


            window2.Close()

         elif timer_running: #esto es para que corra el tiempo
             #  window['-OUTPUT-'].update('{:02d}:{:02d}'.format((counter // 100) // 60, (counter // 100) % 60, counter % 100))
             window['-OUTPUT-'].update('{:02d}:{:02d}'.format((counter // 100) // 60, (counter // 100) % 60))
             counter += 1

             if counter==6000:#6000 equivale a 1 minuto, 60000 a 10 minutos
                timer_running = not timer_running
                sg.Popup('termino el tiempo')

         if event == "Evaluar": # aca va evaluar,evalua la palabra y resetea las orientaciones
             palabra_final = "".join(usados)
             #print(palabra_final)
             vertical = False
             horizontal = False
             ok = verificar_palabra(palabra_final)
             if not ok:
                 for i in range(len(usados)):
                     quitar_fichas(window,usados,botones_usados,no_disponibles)
                 window["puntaje_propio"].update("00")
             else:
                 puntos = puntos_de_palabra(dificult,no_disponibles,puntos)
                 window["puntaje_propio"].update(puntos)
                 usados.clear()
                 #print(puntos)
                 pedir_fichas(window,botones_usados,a,bolsa_total)

    window.Refresh()
    #window.Size=window.Size
#update(atrilNuevo[i])
window.close()
