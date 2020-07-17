import sys
# usamos el import sys para abortar el programa en caso de que los  archivos no
# esten disponibles para ejecutar
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


def botones_De_Fichas(name): return sg.Button(
    name, button_color=color_De_Boton, size=tamanio_Boton_De_Fichas)


def botones_De_Fichas_rival(name): return sg.Button(
    '?', button_color=color_De_Boton, size=tamanio_Boton_De_Fichas)


sg.ChangeLookAndFeel('DarkGrey6')  # thema del PySimpleGUI

# VENTANA PRINCIPAL
opciones_de_inicio = [
    [sg.Button("Comenzar", size=tamanio_Boton_De_Control)],
    [sg.Button("Cargar Partida", size=tamanio_Boton_De_Control)],
    [sg.Button('Configuracion', size=tamanio_Boton_De_Control)],
    [sg.InputCombo(dificultad, default_value='Facil',
                   size=(10, 10), key='dificultad')],
    [sg.Button('Guardar Partida', size=tamanio_Boton_De_Control, visible=False)],
    [sg.Button('Salir', size=tamanio_Boton_De_Control)]
]

# VENTANA DEL JUEGO
opciones_de_juego = [
    [sg.Button('Borrar', size=tamanio_Boton_De_Control),
     sg.Button("Evaluar", size=tamanio_Boton_De_Control),
     sg.Button("Repartir De Nuevo", size=tamanio_Boton_De_Control),
     sg.Button("TOP", size=tamanio_Boton_De_Control)]
]
# FICHAS DEL JUGADOR
fichas = [
    [sg.Text("Tus Fichas: ", font=("Chalkboard", 15))],
    [sg.Button('', button_color=('black', 'oldlace'), size=(tamanio_Boton_De_Fichas), key="Boton_1", pad=(5, 5)),
     sg.Button('', button_color=('black', 'oldlace'), size=(
         tamanio_Boton_De_Fichas), key="Boton_2", pad=(5, 5)),
     sg.Button('', button_color=('black', 'oldlace'), size=(
         tamanio_Boton_De_Fichas), key="Boton_3", pad=(5, 5)),
     sg.Button('', button_color=('black', 'oldlace'), size=(
         tamanio_Boton_De_Fichas), key="Boton_4", pad=(5, 5)),
     sg.Button('', button_color=('black', 'oldlace'), size=(
         tamanio_Boton_De_Fichas), key="Boton_5", pad=(5, 5)),
     sg.Button('', button_color=('black', 'oldlace'), size=(
         tamanio_Boton_De_Fichas), key="Boton_6", pad=(5, 5)),
     sg.Button('', button_color=('black', 'oldlace'), size=(tamanio_Boton_De_Fichas), key="Boton_7", pad=(5, 5))]
]

# FICHAS DEL NPC
fichas_rival = [
    [sg.Text("Fichas CPU: ", font=("Chalkboard", 15))],
    [botones_De_Fichas_rival(j) for j in atril_maquina]
]

tablero = [
    [sg.Button('', button_color=('grey', 'white'), size=(1, 1), key=(i, j), pad=(0, 0)) for j in range(max_Cant_Columnas)] for i in range(max_Cant_Filas)
]  # botones matriz

puntaje_y_tiempo = [
    [sg.Text('TU PUNTAJE:', font=("Chalkboard", 10))], [
        sg.Text('00', key='puntaje_propio', font=("Chalkboard", 10))],
    [sg.Text('PUNTAJE PC: 0', font=("Chalkboard", 10))],
    [sg.Text('Tiempo', font=('Chalkboard', 15))],
    [sg.Text('00:00', font=('Chalkboard', 15), key='-OUTPUT-')],
    [sg.T(' ' * 5)]
]

layout = [
    [sg.Text("Scrabble", size=(8, 1), justification='left',
             font=("Chalkboard", 25), relief=sg.RELIEF_RIDGE)],
    [sg.Column(fichas_rival, key='atrilFichasRival',
               justification='center', visible=False)],
    [sg.Column(opciones_de_inicio, key='opcionesComienzo', justification='left'), sg.Column(
        tablero), sg.Column(puntaje_y_tiempo, key='puntaje', visible=False)],
    [sg.Column(fichas, key='atrilFichas', justification='center', visible=False)],
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
puntos_npc_total = 100
letras_atril_jugador = []     # letras que voy usando
letras_atril_rival = []
letras_usadas_en_tablero = []  # lleva las letras que ya use
botones_usados = []           # nombre de los botones que voy usando
lugares_no_disponibles = []     # lleva la cuenta de los lugares que ya escribi
ant = ()                 # para despintar la casilla anterior cuando toco una nueva
lugar = ()                    # marca la casilla actual
layout2 = layout              # esto no se que es
# cantidad de veces de pedidos para hacer el cambio de fichas totales
cantidad_de_veces_Repartidas = 0
timer_running, counter = False, 0  # seteos para el timer,
dificult = ''         # la dificultad actual que luego sera asignada
h = False
v = False

while True:
    event, values = window.read(timeout=10)
    if event in (None, 'Salir'):
        break
    else:
        if type(event) is tuple:
            lugar = event
            if lugar not in lugares_no_disponibles:  # pinto el lugar que estoy seleccionando,hago esa pregunta para que no trate de marcar un casillero que ya tiene una letra
                window[lugar].update(button_color=('white', 'darkgrey'))
            # digo que si anterior tiene algo que despinte lo anterior
            if (ant) and (ant not in lugares_no_disponibles):
                funciones.volver_a_pintar_la_casilla(lugar, window)
            ant = lugar,

        # si el evento seria una letra y lugar tiene algo es xq marque algo
        if event in ("Boton_1", "Boton_2", "Boton_3", "Boton_4", "Boton_5",
                     "Boton_6", "Boton_7") and lugar:
            letra = window[event].GetText()  # asigno la letra del evento
            if lugar not in lugares_no_disponibles:  # si el lugar no lo use
                # vemos si es la primera letra, seteamos la orientacion
                if len(letras_usadas_en_tablero) == 0:
                    funciones.letra_al_tablero(window, letras_usadas_en_tablero, botones_usados,
                                               letras_atril_jugador, lugares_no_disponibles, letra, event, lugar)

                    # hay que declarar una variable dific para enviar en lugar de facil
                    puntos_jugador += funciones.puntos_de_letra(
                        letra, dificult, lugar)
                    window["puntaje_propio"].update(puntos_jugador)
                # vemos si es la primera letra, seteamos la orientacion de la palabra
                elif len(letras_usadas_en_tablero) == 1:
                    h = funciones.horizontal(
                        lugar, lugares_no_disponibles[len(lugares_no_disponibles)-1])
                    v = funciones.vertical(
                        lugar, lugares_no_disponibles[len(lugares_no_disponibles)-1])
                    funciones.letra_al_tablero(window, letras_usadas_en_tablero, botones_usados,
                                               letras_atril_jugador, lugares_no_disponibles, letra, event, lugar)

                    # hay que declarar una variable dific para enviar en lugar de facil
                    puntos_jugador += funciones.puntos_de_letra(
                        letra, dificult, lugar)
                    window["puntaje_propio"].update(puntos_jugador)
                elif len(letras_usadas_en_tablero) > 1:
                    if funciones.horizontal(lugar, lugares_no_disponibles[len(lugares_no_disponibles)-1]) and h:
                        funciones.letra_al_tablero(window, letras_usadas_en_tablero, botones_usados,
                                                   letras_atril_jugador, lugares_no_disponibles, letra, event, lugar)

                        puntos_jugador += funciones.puntos_de_letra(
                            letra, dificult, lugar)
                        window["puntaje_propio"].update(puntos_jugador)
                    elif funciones.vertical(lugar, lugares_no_disponibles[len(lugares_no_disponibles)-1]) and v:
                        funciones.letra_al_tablero(window, letras_usadas_en_tablero, botones_usados,
                                                   letras_atril_jugador, lugares_no_disponibles, letra, event, lugar)

                        puntos_jugador += funciones.puntos_de_letra(
                            letra, dificult, lugar)
                        window["puntaje_propio"].update(puntos_jugador)
                    else:
                        sg.Popup('Lugar Invalido')

        elif event == "Repartir De Nuevo":  # pide 7 fichas nuevas en la mano
            if not botones_usados:
                cantidad_de_veces_Repartidas = funciones.repartir_fichas_de_nuevo(
                    window, cantidad_de_veces_Repartidas, letras_atril_jugador, bolsa_total)
            else:
                sg.Popup(
                    'Estas en medio de una mano, tenes q tener 7 fichas para cambiar')

        elif event == "Borrar":  # quita elementos del tablero, desde el ultimo al primero
            if puntos_jugador != 0:
                puntos_jugador -= funciones.puntos_de_letra(letras_usadas_en_tablero[len(
                    letras_usadas_en_tablero)-1], dificult, lugares_no_disponibles[len(lugares_no_disponibles)-1])
                window["puntaje_propio"].update(puntos_jugador)
                funciones.quitar_fichas(window, letras_usadas_en_tablero,
                                        botones_usados, lugares_no_disponibles, letras_atril_jugador)

        elif event == "Comenzar":  # para inicializar el juego
            nombre = funciones.carga_nombre()
            timer_running, dificult = funciones.cargar_juego(
                window, values, timer_running, nombre, bolsa_total, letras_atril_jugador, letras_atril_rival)

        elif event == "Cargar Partida":
            dificult, puntos_jugador, puntos_jugador_total, puntos_npc, puntos_npc_total, h, v = funciones.cargar_partida(
                window, letras_atril_jugador, botones_usados, lugares_no_disponibles, l2_guar)

        elif event == "Configuracion":
            funciones.configuracion_de_juego()

        elif event == "TOP":
            with open('./texto/ranking.json', 'r') as r:
                dicc = json.load(r)

            fac = dicc['facil']
            med = dicc['medio']
            dif = dicc['dificil']

            f = sorted(fac.items(), key=lambda k: k[1]["Puntos"], reverse=True)
            m = sorted(med.items(), key=lambda k: k[1]["Puntos"], reverse=True)
            d = sorted(dif.items(), key=lambda k: k[1]["Puntos"], reverse=True)

            rank_facil = funciones.formet(dict(f))
            rank_medio = funciones.formet(dict(m))
            rank_dif = funciones.formet(dict(d))

            tab1_layout = [[sg.T('This is inside tab 1')]]
            tab2_layout = [[sg.Listbox(values=rank_facil, size=(30, 10))]]
            tab3_layout = [[sg.Listbox(values=rank_medio, size=(30, 10))]]
            tab4_layout = [[sg.Listbox(values=rank_dif, size=(30, 10))]]

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
                if event2 == 'Exit':
                    break
            window2.Close()

        elif timer_running:  # esto es para que corra el tiempo
            #  window['-OUTPUT-'].update('{:02d}:{:02d}'.format((counter // 100) // 60, (counter // 100) % 60, counter % 100))
            window['-OUTPUT-'].update('{:02d}:{:02d}'.format(
                (counter // 100) // 60, (counter // 100) % 60))
            counter += 1

            if counter == 6000:  # 6000 equivale a 1 minuto, 60000 a 10 minutos
                timer_running = not timer_running
                sg.Popup('termino el tiempo,analizando ganador:')
                if puntos_jugador_total > puntos_npc_total:
                    sg.Popup('¡Ganaste!')
                elif puntos_jugador_total == puntos_npc_total:
                    sg.Popup('¡Hubo un empate!')
                else:
                    sg.Popup('¡YOU DIED!,GIT GUD M8')
                sys.exit()
        if event == "Evaluar":  # aca va evaluar,evalua la palabra y resetea las orientaciones
            palabra_final = "".join(letras_usadas_en_tablero)
            v = False
            h = False
            if funciones.verificar_palabra(palabra_final):
                print("palabra valida")
                puntos_jugador_total = funciones.puntos_de_palabra(
                    dificult, lugares_no_disponibles, puntos_jugador)
                window["puntaje_propio"].update(puntos_jugador_total)
                l2_guar.extend(letras_usadas_en_tablero)
                letras_usadas_en_tablero.clear()
                puntos_jugador = 0
                funciones.pedir_fichas(
                    window, botones_usados, letras_atril_jugador, bolsa_total)
            else:
                print("palabra invalida")
                for i in range(len(letras_usadas_en_tablero)):
                    funciones.quitar_fichas(
                        window, letras_usadas_en_tablero, botones_usados, lugares_no_disponibles, letras_atril_jugador)
                window["puntaje_propio"].update("00")

        if event == "Guardar Partida":
            if not botones_usados:
                with open('./texto/save.json', 'w') as j:
                    dic = {}
                    dic["puntos"] = {"puntos_jugador": puntos_jugador, "puntos_jugador_total": puntos_jugador_total,
                                     "puntos_npc": puntos_npc, "puntos_npc_total": puntos_npc_total}
                    dic["atril"] = {"atril_jugador": letras_atril_jugador}
                    dic["otros"] = {"lugares": lugares_no_disponibles,
                                    "letras_usadas": l2_guar, "dificultad": dificult, "hor": h, "ver": v}
                    json.dump(dic, j, indent=4)
            else:
                sg.Popup(
                    "Solo se puede guardar una partida teniendo el atril completo")
    window.Refresh()
window.close()
