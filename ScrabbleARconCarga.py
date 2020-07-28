import sys
import os
# usamos el import sys para abortar el programa en caso de que los  archivos no
# esten disponibles para ejecutar
import random
import json
import PySimpleGUI as sg
from funciones import funciones

# INICIA EL PROGRAMA PRINCIPAL

try:
    with open('./texto/config.json', 'r') as cf:
        pass
except FileNotFoundError:
    sg.Popup('ERROR ---> config.json NO ENCONTRADO')
    sys.exit()

bolsa_total = funciones.crear_bolsita_total()

atril_maquina = funciones.crear_atril(bolsa_total)

color_De_Boton = ('Black', 'seagreen')
tamanio_Boton_De_Fichas = 2, 2  # tamanio de botones que seran las fichas
tamanio_Boton_De_Control = 15, 1  # tamanio de botones de comenzar y salir
max_Cant_Filas = max_Cant_Columnas = 15  # tamanio de las matrices
dificultad = ['Facil', 'Medio', 'Dificil']  # combobox


sg.ChangeLookAndFeel('DarkGrey6')  # thema del PySimpleGUI

# VENTANA PRINCIPAL
opciones_de_inicio = [
    [sg.Button("Comenzar", size=tamanio_Boton_De_Control)],
    [sg.Button("Cargar Partida", size=tamanio_Boton_De_Control)],
    [sg.Button('Configuracion', size=tamanio_Boton_De_Control)],
    [sg.InputCombo(dificultad, default_value='Facil',
                   size=(10, 10), key='dificultad')],
    [sg.Button("TOP", size=tamanio_Boton_De_Control)],                   
    [sg.Button('Guardar Partida', size=tamanio_Boton_De_Control,
               visible=False)],
    [sg.Button('Salir', size=tamanio_Boton_De_Control)]
]

# VENTANA DEL JUEGO
opciones_de_juego = [
    [sg.Button('Borrar', size=tamanio_Boton_De_Control),
     sg.Button("Evaluar", size=tamanio_Boton_De_Control),
     sg.Button("Repartir De Nuevo", size=tamanio_Boton_De_Control)
    ]
]

# FICHAS DEL JUGADOR
fichas = [[sg.Text("Tus Fichas: ", font=("Chalkboard", 15))],
          [sg.Button('', button_color=('black', 'oldlace'),
                     size=(tamanio_Boton_De_Fichas),
                     key=("Boton_"+str(i+1)), pad=(5, 5)) for i in range(7)]
          ]

# FICHAS DEL NPC
fichas_rival = [[sg.Text("Fichas CPU: ", font=("Chalkboard", 15))],
                [sg.Button('??', size=(
                    tamanio_Boton_De_Fichas), key=("Boton_2_"+str(i+1)),
                    pad=(5, 5)) for i in range(7)]
                ]

botones_indieces=[[sg.Button(size=(1,1),button_color=('black', 'indianred')),sg.Text('Letra +5')],
                  [sg.Button(size=(1,1),button_color=('black', 'skyblue')),sg.Text('Palabra /2')],
                  [sg.Button(size=(1,1),button_color=('black', 'goldenrod')),sg.Text('Letra *2')], 
                  [sg.Button(size=(1,1),button_color=('black', 'mediumseagreen')),sg.Text('Palabra -(0,10)')],
                  ]



tablero = [
    [sg.Button('', button_color=('grey', 'white'), size=(1, 1), key=(i, j),
               pad=(0, 0)) for j in range(max_Cant_Columnas)] for i in range(max_Cant_Filas)
]  # botones matriz

puntaje_y_tiempo = [
    [sg.Text(' ------ TU PUNTAJE ES:', key='tu_puntaje_propio', size=(20, 1),
             font=("Chalkboard", 10))],
    [sg.Text('0', key='puntaje_propio', font=("Chalkboard", 10))],
    [sg.Text('PUNTAJE DE JUGADA:', font=("Chalkboard", 10))],
    [sg.Text('0', key='puntaje_de_jugada', font=("Chalkboard", 10))],
    [sg.Text('PUNTAJE PC:', font=("Chalkboard", 10))],
    [sg.Text('0', key='puntaje_PC', font=("Chalkboard", 10))],
    [sg.Text('Tiempo', font=('Chalkboard', 15))],
    [sg.Text('00:00', font=('Chalkboard', 15), key='-OUTPUT-')],
    [sg.T(' ' * 5)]
]

layout = [
    [sg.Text("Scrabble", size=(8, 1), justification='left',
             font=("Chalkboard", 25), relief=sg.RELIEF_RIDGE)],
    [sg.Column(fichas_rival, key='atrilFichasRival',
               justification='center', visible=False)],
    [sg.Column(opciones_de_inicio, key='opcionesComienzo',
               justification='left'), sg.Column(tablero),
     sg.Column(puntaje_y_tiempo, key='puntaje', visible=False),
     sg.Frame('Valores de celdas', botones_indieces,key='indice', visible=False)],
    [sg.Column(fichas, key='atrilFichas', justification='center',
               visible=False)],
    [sg.Column(opciones_de_juego, key='opcionesJuego',
               justification='center', visible=False)],
]

window = sg.Window('SCRABBLE', layout, default_button_element_size=(
    2, 2), finalize=True, resizable=True,  auto_size_buttons=True)

l2_guar = []
# puntos del jugdador,(en realidad hay que tener 2)
puntos_jugador = 0
puntos_jugador_total = 0
puntos_npc = 0
puntos_npc_total = 0
letras_atril_jugador = []     # letras que voy usando
letras_atril_rival = []
letras_usadas_en_tablero = []  # lleva las letras que ya use
botones_usados = []           # nombre de los botones que voy usando
lugares_no_disponibles = []     # lleva la cuenta de los lugares que ya escribi
# para despintar la casilla anterior cuando toco una nueva
ant = ()
lugar = ()                    # marca la casilla actual
layout2 = layout              # esto no se que es
# cantidad de veces de pedidos para hacer el cambio de fichas totales
cantidad_de_veces_Repartidas = 0
timer_running, counter = False, 0  # seteos para el timer,
dificult = ''         # la dificultad actual que luego sera asignada
h = False
v = False
turno = ''

funciones.dibujo_python(window)


while True:
    event, values = window.read(timeout=10)
    #print(event)
    if event in (None, 'Salir'):
        break
    else:

        if turno == 'player_2':
            puntos_npc, turno = funciones.turno_maquina(window, letras_atril_rival,
                                                        lugar, lugares_no_disponibles,
                                                        turno, bolsa_total,
                                                        letras_usadas_en_tablero,
                                                        dificult, l2_guar)
            puntos_npc_total = puntos_npc_total+puntos_npc
            window["puntaje_PC"].update(puntos_npc_total)
            print('turno vuelta', turno)
            sg.Popup('Tu Turno!')
        if type(event) is tuple:
            lugar = event
            # pinto el lugar que estoy seleccionando,hago esa pregunta para
            # que no trate  de marcar un casillero que ya tiene una letra
            if lugar not in lugares_no_disponibles:
                window[lugar].update(button_color=('white', 'darkgrey'))
                print(lugar)
            # digo que si anterior tiene algo que despinte lo anterior
            if (ant) and (ant not in lugares_no_disponibles):
                funciones.volver_a_pintar_la_casilla(lugar, window, dificult)
            ant = lugar

        # si el evento seria una letra y lugar tiene algo es xq marque algo
        if event in ("Boton_1","Boton_1", "Boton_2", "Boton_3", "Boton_4", 
                     "Boton_5", "Boton_6", "Boton_7") and lugar:
            letra = window[event].GetText()  # asigno la letra del evento
            if lugar not in lugares_no_disponibles:  # si el lugar no lo use
                # vemos si es la primera letra, seteamos la orientacion
                if len(letras_usadas_en_tablero) == 0:
                    funciones.letra_al_tablero(window,
                                               letras_usadas_en_tablero,
                                               botones_usados,
                                               letras_atril_jugador,
                                               lugares_no_disponibles, letra,
                                               event, lugar)

                    # hay que declarar una variable dific para enviar
                    # en lugar de facil
                    puntos_jugador += funciones.puntos_de_letra(
                        letra, dificult, lugar)
                    window["puntaje_de_jugada"].update(puntos_jugador)
                # vemos si es la primera letra, seteamos la orientacion de
                #  la palabra
                elif len(letras_usadas_en_tablero) == 1:
                    h = funciones.horizontal(
                        lugar, lugares_no_disponibles
                        [len(lugares_no_disponibles)-1])
                    v = funciones.vertical(
                        lugar, lugares_no_disponibles
                        [len(lugares_no_disponibles)-1])
                    funciones.letra_al_tablero(window,
                                               letras_usadas_en_tablero,
                                               botones_usados,
                                               letras_atril_jugador,
                                               lugares_no_disponibles, letra,
                                               event, lugar)

                    # hay que declarar una variable dific para enviar en lugar
                    # de facil
                    puntos_jugador += funciones.puntos_de_letra(
                        letra, dificult, lugar)
                    window["puntaje_de_jugada"].update(puntos_jugador)
                elif len(letras_usadas_en_tablero) > 1:
                    if funciones.horizontal(lugar, lugares_no_disponibles
                                            [len(lugares_no_disponibles)-1]) and h:
                        funciones.letra_al_tablero(window,
                                                   letras_usadas_en_tablero,
                                                   botones_usados,
                                                   letras_atril_jugador,
                                                   lugares_no_disponibles,
                                                   letra, event, lugar)

                        puntos_jugador += funciones.puntos_de_letra(
                            letra, dificult, lugar)
                        window["puntaje_de_jugada"].update(puntos_jugador)
                    elif funciones.vertical(lugar, lugares_no_disponibles
                                            [len(lugares_no_disponibles)-1]) and v:
                        funciones.letra_al_tablero(window,
                                                   letras_usadas_en_tablero,
                                                   botones_usados,
                                                   letras_atril_jugador,
                                                   lugares_no_disponibles,
                                                   letra, event, lugar)

                        puntos_jugador += funciones.puntos_de_letra(
                            letra, dificult, lugar)
                        window["puntaje_de_jugada"].update(puntos_jugador)
                    else:
                        sg.Popup('Lugar Invalido')
        # pide 7 fichas nuevas en la mano
        elif event == "Repartir De Nuevo":
            if not botones_usados:
                cantidad_de_veces_Repartidas = funciones.repartir_fichas_de_nuevo(
                    window, cantidad_de_veces_Repartidas, letras_atril_jugador,
                    bolsa_total)
            else:
                sg.Popup(
                    'Estas en medio de una mano, tenes q tener 7 fichas para',
                    ' cambiar')
        # quita elementos del tablero, desde el ultimo al primero
        elif event == "Borrar":
            if puntos_jugador != 0:
                puntos_jugador -= funciones.puntos_de_letra(letras_usadas_en_tablero[len(
                    letras_usadas_en_tablero)-1], dificult,
                    lugares_no_disponibles[len(lugares_no_disponibles)-1])
                window["puntaje_de_jugada"].update(puntos_jugador)
                funciones.quitar_fichas(window, letras_usadas_en_tablero,
                                        botones_usados, lugares_no_disponibles,
                                        letras_atril_jugador, dificult)

        # para inicializar el juego
        elif event == "Comenzar":
            nombre = funciones.carga_nombre()
            [[window[i, j].update(button_color=('black', 'azure')) for j in range(max_Cant_Columnas)] for i in range(max_Cant_Filas)]
            timer_running, dificult = funciones.cargar_juego(
                window, values, timer_running, nombre, bolsa_total,
                letras_atril_jugador, letras_atril_rival)
            # random para ver quien inicia la partida
            quien_inicia = random.choice(range(1, 3))
            turno = 'player_'+str(quien_inicia)
            if turno == 'player_1':
                try:
                    sg.popup('Empezas vos {}!'.format(nombre.upper()))
                except AttributeError:
                    nombre = 'NN'    
                    sg.popup('Empezas vos {}!'.format(nombre.upper()))
            else:
                sg.popup('Comienza la maquina!')

        elif event == "Cargar Partida":
            if os.path.isfile('./texto/save.json') :   
                counter, dificult, puntos_jugador, puntos_jugador_total, puntos_npc, puntos_npc_total, h, v = funciones.cargar_partida(
                    window, letras_atril_jugador, botones_usados, lugares_no_disponibles, l2_guar, letras_atril_rival)
                timer_running = not timer_running
            else:  
                sg.popup('No tenes partidas guardadas')



        elif event == "Configuracion":
            funciones.configuracion_de_juego()

        elif event == "TOP":
            with open('./texto/ranking_test.json', 'r') as r:
                dicc = json.load(r)

            fac={}
            med={}
            dif={}
            for k, v in dicc.items():
                if v["Dificultad"]=='facil':
                    fac[k] = v 
                elif v["Dificultad"]=='medio':
                    med[k] = v      
                elif v["Dificultad"]=='dificil':
                    dif[k] = v      

            f = sorted(fac.items(), key=lambda k: k[1]["Puntos"], reverse=True)
            m = sorted(med.items(), key=lambda k: k[1]["Puntos"], reverse=True)
            d = sorted(dif.items(), key=lambda k: k[1]["Puntos"], reverse=True)
            total=  sorted(dicc.items(), key=lambda k: k[1]["Puntos"], reverse=True)

            print(total)

            rank_facil = funciones.formet(dict(f))
            rank_medio = funciones.formet(dict(m))
            rank_dif = funciones.formet(dict(d))
            rank_total = funciones.formet(dict(total))

            tab1_layout = [[sg.Listbox(values=rank_total, size=(50, 10))]]
            tab2_layout = [[sg.Listbox(values=rank_facil, size=(50, 10))]]
            tab3_layout = [[sg.Listbox(values=rank_medio, size=(50, 10))]]
            tab4_layout = [[sg.Listbox(values=rank_dif, size=(50, 10))]]

            layout2 = [
                [sg.Text('RANKING'), sg.Text('', key='_OUTPUT_')],
                [sg.TabGroup([
                    [sg.Tab('Ranking General', tab1_layout, tooltip='tip'),
                     sg.Tab('Ranking Facil', tab2_layout, tooltip='tip2'),
                     sg.Tab('Ranking Medio', tab3_layout, tooltip='tip3'),
                     sg.Tab('Ranking Dificil', tab4_layout, tooltip='tip4')]
                ])],
                [sg.Button('Exit')]
            ]
            window2 = sg.Window('TOP TEN').Layout(layout2)
            while True:
                event2, values2 = window2.Read()
                if event2 == 'Exit' or event2 == None:
                    break
            window2.Close()

        # esto es para que corra el tiempo
        elif timer_running:
            # window['-OUTPUT-'].update('{:02d}:{:02d}'.format((counter // 100)
            # // 60, (counter // 100) % 60, counter % 100))
            window['-OUTPUT-'].update('{:02d}:{:02d}'.format(
                (counter // 100) // 60, (counter // 100) % 60))
            counter += 1

            # 6000 equivale a 1 minuto, 60000 a 10 minutos
            if counter == 6000:
                timer_running = not timer_running
                sg.Popup('termino el tiempo,analizando ganador:')
                if puntos_jugador_total > puntos_npc_total:
                    sg.Popup('¡Ganaste!')
                    with open('./texto/ranking_test.json', 'r') as j:
                        dicc = json.load(j)
                    with open('./texto/ranking_test.json', 'w') as j:
                        id=str(random.choice(range(0,10000)))
                        dicc['id_'+id] = {"Dificultad": dificult.lower(),
                                         "Nombre":nombre,
                                         "Puntos": puntos_jugador_total,
                                         "Fecha": 0}

                        json.dump(dicc, j, indent=4)                 
                  
                    
                elif puntos_jugador_total == puntos_npc_total:
                    sg.Popup('¡Hubo un empate!')
                else:
                    sg.Popup('¡YOU DIED!,GIT GUD M8')
                sys.exit()

        # aca va evaluar,evalua la palabra y resetea las orientaciones
        if event == "Evaluar":
            palabra_final = "".join(letras_usadas_en_tablero)
            v = False
            h = False
            if funciones.verificar_palabra(palabra_final):
                lista_coords = []
                tamanio_pal = len(palabra_final)
                for i in range(1, tamanio_pal+1):
                    element = lugares_no_disponibles[-i]
                    lista_coords.append(element)
                lista_coords.reverse()
                # print("palabra valida")
                puntos_jugador_total_aux = funciones.puntos_de_palabra(
                    dificult, lista_coords, puntos_jugador)
                puntos_jugador_total += puntos_jugador_total_aux
                # print('total',puntos_jugador_total )
                # print('total auzx',puntos_jugador_total_aux )
                # print('puntos_jugador',puntos_jugador)
                window["puntaje_propio"].update(puntos_jugador_total)
                l2_guar.extend(letras_usadas_en_tablero)
                letras_usadas_en_tablero.clear()
                puntos_jugador = 0
                window["puntaje_de_jugada"].update("0")
                funciones.pedir_fichas(
                    window, botones_usados, letras_atril_jugador, bolsa_total)
                turno = 'player_2'
            else:
                print("palabra invalida")
                for i in range(len(letras_usadas_en_tablero)):
                    funciones.quitar_fichas(
                        window, letras_usadas_en_tablero, botones_usados,
                        lugares_no_disponibles, letras_atril_jugador,dificult)
                window["puntaje_de_jugada"].update("0")
                puntos_jugador = 0

        if event == "Guardar Partida" and turno == 'player_1':
            if not botones_usados:
                with open('./texto/save.json', 'w') as j:
                    dic = {}
                    dic["nombre"] = nombre
                    dic["puntos"] = {"puntos_jugador": puntos_jugador,
                                     "puntos_jugador_total":
                                     puntos_jugador_total,
                                     "puntos_npc": puntos_npc,
                                     "puntos_npc_total": puntos_npc_total}
                    dic["atril"] = {"atril_jugador": letras_atril_jugador}
                    dic["atril_rival"] = {
                        "letras_atril_rival": letras_atril_rival}
                    dic["otros"] = {"lugares": lugares_no_disponibles,
                                    "letras_usadas": l2_guar,
                                    "dificultad": dificult, "hor": h, "ver": v}
                    dic['tiempo'] = {'reloj': counter}
                    json.dump(dic, j, indent=4)
            else:
                sg.Popup(
                    "Solo se puede guardar una partida teniendo",
                    "el atril completo")
    window.Refresh()
window.close()
