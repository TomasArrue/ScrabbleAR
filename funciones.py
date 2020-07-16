import sys  # usamos el import sys para abortar el programa en caso de que los archivos no esten disponibles para ejecutar
import json
import PySimpleGUI as sg
import random
from string import ascii_uppercase as up
from random import choice
from pattern.text.es import lexicon,spelling,verbs

######## LE MANDO TODOS LOS IMPORTS DESPUES VEO CUAL QUEDA Y CUAL SE VA ########


def configuracion_de_juego():
    """
        configuracion del juego inicial,cargamos el config.json, para poder cambiar
        la cantidades de letras iniciales en la bolsa de fichas y ademas podemos
        editar el valor de cada ficha
    """
    with open('config.json','r') as cf:
        c = json.load(cf)

    diccionario_cantidad_de_letras = c['cantidad_de_letras']
    diccionario_cantidad_de_puntos = c['valor_por_letra']

    layout3 = [
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
                    num_tiempo = 30
                if ( num_tiempo < 5 ):
                    num_tiempo = 5
            except (ValueError):
                    num_tiempo = 15 # seteamos 15 minutos en caso de cargar erronea, pero informamos que se cargo mal el tiempo
                    sg.Popup('El tiempo se cargo de maneara erronea, pero cargamos la partida de 15 minutos')
            for k,v in diccionario_cantidad_de_letras.items():
                try:
                    numero_nuevo = int(values3[k+'_cant'])
                except (ValueError):
                    numero_nuevo = 1
            sg.Popup('La duracion de la partida sera de: ',num_tiempo,' minutos')
    window3.close()


def crear_bolsita_total():
    """
        Generamos la bolsas con las fichas totales para usar en el juego,
        las cuales tenemos almacenadas en el config.json
    """
    with open('./texto/config.json','r') as cf:
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
    layout3 = [
    [sg.Text('Ingresa tu nombre:')],
    [sg.Input('',key='name')],
    [sg.Button('Listo')]
    ]
    window3 = sg.Window('Ingresa datos',layout3)
    while True:
         event,values = window3.read()
         if event == 'Listo':
             nombre = values['name']
             break
    window3.close()

    return nombre


def asignar_colores_al_tablero(window,dificultad):
    """
       Se van a pintar los botones de la matriz que conforman el tablero
       segun las coordenas que vengan en el archivo json, dependiendo
       el nivel que hayamos elegido
    """
    with open('./texto/config.json','r') as t:
        dic = json.load(t)

    #print(dificultad)
    tablero_config = dic[dificultad]

    for colores in tablero_config.keys():
        lista_de_cord = tablero_config[colores]
        for par_de_cord in lista_de_cord:
            x,y = par_de_cord
            window[x,y].update(button_color=(colores,colores))


def cargar_juego(window,values,timer_running,nombre,bolsa_total,letras_atril_jugador,letras_atril_rival):
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
        obtener_fichas(window,nro_de_boton,letras_atril_jugador,bolsa_total)
        letra_rival = crear_atril(bolsa_total)  #generamos las fichas del rival tambien
        letras_atril_rival.append(letra_rival)  #Las agregamos a su lista

    timer_running = not timer_running

    return timer_running, very_dificult


def cargar_partida(window,letras_atril_jugador,botones_usados,lugares_no_disponibles):
    """
       asdasd
    """

    l2 = []
    with open('save.json','r') as l:
        dic = json.load(l)
    asignar_colores_al_tablero(window,dic["otros"]["dificultad"])
    window['opcionesJuego'].update(visible=True)
    window['Comenzar'].update(visible=False)
    window['Configuracion'].update(visible=False)
    window['Cargar Partida'].update(visible=False)
    window['Guardar Partida'].update(visible=True)
    window['Salir'].update(visible=True)
    window['puntaje_propio'].update("PUNTAJE DE {0} ES :0".format("pepe"))
    window['puntaje'].update(visible=True)
    window["puntaje_propio"].update(dic["puntos"]["puntos_jugador_total"])
    window['atrilFichasRival'].update(visible=True)
    window['atrilFichas'].update(visible=True)
    window['dificultad'].update(visible=False)

    for i in range(len(dic["atril"]["atril_jugador"])):  # carga de las 7 fichas al inicio
        nro_de_boton='Boton_'+str(i+1)
        letras_atril_jugador.append(dic["atril"]["atril_jugador"][i])
        window[nro_de_boton].update(dic["atril"]["atril_jugador"][i])

    for i in range(len(dic["otros"]["lugares"])):
        lugares_no_disponibles.append(tuple(dic["otros"]["lugares"][i]))
        window[lugares_no_disponibles[i]].update(dic["otros"]["letras_usadas"][i],button_color=('black','oldlace'))

    for butt in dic["otros"]["boton"]:
        botones_usados.append(butt)

    return dic["otros"]["dificultad"],dic["puntos"]["puntos_jugador"],dic["puntos"]["puntos_jugador_total"],dic["puntos"]["puntos_npc"],dic["puntos"]["puntos_npc_total"],dic["otros"]["hor"],dic["otros"]["ver"]


def volver_a_pintar_la_casilla(cord,window):
    """
        este modulo nos sirve para volver a pintar un boton de su color inicial
        en caso de que tengamos que sacar una ficha que pusimos
    """
    with open ('./texto/config.json','r') as p:
        dicc = json.load(p)
    # la dific tiene que vernir como parametro para saber que tablero abrir
    tablero_actual = dicc["Facil"]

    if list(cord) in tablero_actual["indianred"]:
         window[cord].update(button_color=('indianred','indianred'))
    elif list(cord) in tablero_actual["goldenrod"]:
         window[cord].update(button_color=('goldenrod','goldenrod'))
    elif list(cord) in tablero_actual["mediumseagreen"]:
         window[cord].update(button_color=('mediumseagreen','mediumseagreen'))
    elif list(cord) in tablero_actual["skyblue"]:
         window[cord].update(button_color=('skyblue','skyblue'))
    else:
         window[cord].update(button_color=('grey','white'))

def verificar_palabra(palabra):
    """
        verificamos si la palabra es valida
    """
    if palabra in lexicon and spelling or palabra in verbs:
        return(True)
    else:
        return(True) #cambiar a false


def obtener_fichas(window,nro_de_boton,letras_atril_jugador,bolsa_total):
    """
        Este metodo nos da una ficha "nueva".
        Generamos una letra random la agregamos a la lista de letras de nuestro atril,
        luego con la key del boton recibida como parametro actualizamos el valor del
        boton con la nueva letra
    """
    letra = crear_atril(bolsa_total)
    letras_atril_jugador.append(letra)
    window[nro_de_boton].update(letra)
    window[nro_de_boton].update(button_color=('black','oldlace'))
    window.Refresh()


def repartir_fichas_de_nuevo(window,cantidad_de_veces_Repartidas,letras_atril_jugador,bolsa_total):
    """
        Utilizamos este metodo para poder cambiar la mano de fichas que tenemos,
        y tenemos permitido hacerlo hasta 3 veces
    """
    letras_atril_jugador = []
    if (cantidad_de_veces_Repartidas < 3):
        cantidad_de_veces_Repartidas=cantidad_de_veces_Repartidas+1
        for i in range(7):#carga de las 7 fichas
            nro_de_boton='Boton_'+str(i+1)
            obtener_fichas(window,nro_de_boton,letras_atril_jugador,bolsa_total)
    else:
        sg.Popup('Ya hiciste el maximo de cambios de mano')

    return cantidad_de_veces_Repartidas


def quitar_fichas(window,usados,botones_usados,no_disponibles,letras_atril_jugador):
    """
        quitar fichas nos permite sacar las fichas ingresadas al tablero en el turno correspondiente.
        Mientras que la longitud lista de usados del turno sea mayor a 0 vamos a poder retirar fichas
        que ingresamos, en caso de que no se pueda no podremos quitar mas
    """
    # print(len(usados),' ',len(no_disponibles),' ',len(botones_usados))
    if len(usados) > 0:                                  # Aca antes de borrar una letra vamos a preguntar si hay letras para borrar, en caso contrario no podras borrar mas letras
        letra_a_borrar = usados.pop()   # Saca la ultima letra de la palabra cargada - el pop saca de usados  el elemento de la ultima posicion de la lista de usados
        boton_a_recuperar = botones_usados.pop()
        letras_atril_jugador.append(letra_a_borrar)                       # vuelve a cargar la letra que sacamos del tablero en el atril de nuestras fichas
        coord_a_liberar = no_disponibles.pop() # Saca la ultima coordenada de la palabra cargada - el pop saca de no_disponibles el elemento de la ultima posicion de la lista de no_disponibles
        volver_a_pintar_la_casilla(coord_a_liberar,window) # vuelve a pintar la casilla de su color en estado inicial
        window[coord_a_liberar].update("")
        window[boton_a_recuperar].update(button_color=('black','oldlace'),disabled=False)
    else:
        sg.Popup('No hay fichas para borrar')


def pedir_fichas(window,botones_usados,letras_atril_jugador,bolsa_total):
    """
       El pedir fichas nos permite pedir la cantidad de fichas usadas en el ultimo turno
       hasta llegar a tener 7 nuevamente.
    """
    for i in botones_usados:
        letra = letras_atril_jugador[len(letras_atril_jugador)-1]
        window[i].update(letra,disabled = False)
        obtener_fichas(window,i,letras_atril_jugador,bolsa_total)
    for i in range (len(botones_usados)):
        botones_usados.pop()


def letra_al_tablero(window,usados,botones_usados,letras_atril_jugador,no_disponibles,letra,event,lugar):
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
    letras_atril_jugador.remove(letra)
    window[event].update(button_color=('darkgrey','darkgrey'),disabled = True)
    no_disponibles.append(lugar)


def puntos_de_letra(letra,dificultad,coord):
    """
       calculamos el valor de la letra ingresada en el tablero. accedemos al json para ver su puntaje asociado
    """
    with open ('./texto/config.json','r') as p:
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
    with open ('./texto/config.json','r') as p:
        dicc = json.load(p)
    tablero_actual = dicc[dificultad]

    # conjuntos para hacer la interseccion
    green = set(map(tuple,tablero_actual["mediumseagreen"]))
    blue = set(map(tuple,tablero_actual["skyblue"]))

    int_green = green.intersection(set(no_disponibles))
    int_blue = blue.intersection(set(no_disponibles))

    for element in int_green:
        puntos = puntos - random.randint(0,10)
    for element in int_blue:
        puntos =  puntos / 2

    return puntos

def formet(d):
    l = []
    for k,v in d.items():
        variable = '{} {} '.format("Jugador:",k) + '{} {} '.format("Puntaje:",v["Puntos"]) + '{} {}'.format("Fecha:",v["Fecha"])
        l.append(variable)
    return l

def vertical(pos_actual,pos_anterior):

    if pos_anterior[0]+1 == pos_actual[0] and pos_actual[1] == pos_anterior[1]:
        return True
    else:
        return False

def horizontal(pos_actual,pos_anterior):

    if pos_anterior[0] == pos_actual[0] and pos_actual[1] == pos_anterior[1]+1:
        return True
    else:
        return False


############# IA ###############

def validar_palabra(permutaciones,permutaciones_validas):
    '''
        Valida palabras que esten dentro de las permutaciones
        pasadas por parametro y las agrega a una lista de palabras
        validas
    '''
    for pal in permutaciones:
        if pal in verbs or ((pal in lexicon) and (pal in spelling)):
            permutaciones_validas.append(pal) # si la palabra es valida va a la lista de permutaciones
    return permutaciones_validas

def buscar_palabras_rival(letras_atril_rival):
    '''
        recibe el las fichas del atril del rival y genera una lista de
        palabras validas
    '''
    permutaciones_validas=[]# lista para guardar las permutaciones validas
    for i in range(len(letras_atril_rival)):
       if (i+1>=2): # este if es para empezar a armar permutaciones de al menos dos caracteres
            permutaciones_temp={"".join(p) for p in permutations(letras_atril_rival,i+1)} # generamos permutaciones con i+1 caracteres
            validar_palabra(permutaciones_temp,permutaciones_validas) # vemos cuales de esas permutaciones son validas, y las vamos guardando en una lista
    return permutaciones_validas

def buscar_lugar_disponible(window,letras_atril_rival,lugar,lugares_no_disponibles,cant,bolsa_total):
    letras_atril_rival=[x.lower() for x in letras_atril_rival]# pasa la lista a minusculas xq las permutaciones no las reconocen
    print(letras_atril_rival)

    palabras_posibles=buscar_palabras_rival(letras_atril_rival) # buscamos las posibles palabras
    print(palabras_posibles)
    #cantidad_de_veces_Repartidas=1
    try:
        palabra_a_colocar=random.choice(palabras_posibles) # obtenemos alguna de las palabras posibles de la lista al azar si es posible
        ok=False
        while (not ok)&(cant<3):
            x=random.choice(range(0,14))
            y=random.choice(range(0,14))
            lugar=(x,y)
            cant+=1
            print('palabra_a_colocar',palabra_a_colocar)
            if lugar not in lugares_no_disponibles:
                if ((len(palabra_a_colocar)+y) <= 14):# vemos si la palabra puede colocarse verticalmente u horizontalmente
                    ok=True
                    for l in palabra_a_colocar:
                        letras_usadas_en_tablero.append(l)
                        #botones_usados.append(event)
                        window[lugar].update(l.upper(), button_color=('black','oldlace'))
                        letras_atril_rival.remove(l)
                        lugares_no_disponibles.append(lugar)
                        y+=1
                        lugar=(x,y)
                else:
                    if ((len(palabra_a_colocar)+x) <= 14):
                        ok=True
                        for l in palabra_a_colocar:
                            letras_usadas_en_tablero.append(l)
                            #botones_usados.append(event)
                            window[lugar].update(l.upper(), button_color=('black','oldlace'))
                            letras_atril_rival.remove(l)
                            lugares_no_disponibles.append(lugar)
                            x+=1
                            lugar=(x,y)
        print('lugares_no_disponibles',lugares_no_disponibles)
        print('letras_atril_rival',letras_atril_rival)
        print('letras_usadas_en_tablero',letras_usadas_en_tablero)
        for i in range(len(letras_usadas_en_tablero)):
            letra = crear_atril(bolsa_total)
            letras_atril_jugador.append(letra)
        letras_usadas_en_tablero.clear()
        print('letras_atril_rival despues de carga',letras_atril_rival)
    except (IndexError):
        print('no hay palabras validas en la lista')
        '''
        letras_atril_rival.clear
        print('antes',letras_atril_rival)
        for i in range(7):  # carga de las 7 fichas al inicio
            letra_rival = crear_atril(bolsa_total)  #generamos las fichas del rival tambien
            letras_atril_rival.append(letra_rival)  #Las agregamos a su lista
        print('despues',letras_atril_rival)
        '''



def turno_maquina(window,letras_atril_rival,lugar,lugares_no_disponibles,turno,bolsa_total):
    sg.Popup('Turno de la maquina')
    cant=0
    buscar_lugar_disponible(window,letras_atril_rival,lugar,lugares_no_disponibles,cant,bolsa_total)
    return 'player_1'








############## fin IA ###################
