import sys
import os
# usamos el import sys para abortar el programa en caso de que los  archivos no
# esten disponibles para ejecutar
import random
import json
import PySimpleGUI as sg
from funciones import funciones, ia, interfase, ranking
import time
from datetime import date


def test_de_archivo():
    '''
        solo para testear si se encuentra el config.json con todos los datos
        necesarios para que corra el juego, en caso que no se encuentre
        se aborta el programa y se informa de la falta del archivo
    '''
    try:
        with open('./texto/config.json', 'r'):
            pass
    except FileNotFoundError:
        sg.Popup('ERROR ---> config.json NO ENCONTRADO')
        sys.exit()


def iniciar_juego():

    # INICIA EL PROGRAMA PRINCIPAL

    # TAMANIO DE LA MATRIZ
    max_Cant_Filas = max_Cant_Columnas = 15

    test_de_archivo()

    bolsa_total = funciones.crear_bolsita_total()
    total_letras = 0
    for k, v in bolsa_total.items():
        total_letras += v

    # atril_maquina = funciones.crear_atril(bolsa_total)

    # TEMA DEL PySimpleGUI
    sg.ChangeLookAndFeel('DarkGrey6')

    # VENTANA PRINCIPAL
    opciones_de_inicio = interfase.ventan_principal()

    # VENTANA DEL JUEGO
    opciones_de_juego = interfase.ventana_opciones_de_juego()

    # FICHAS DEL JUGADOR
    fichas = interfase.fichas_propias()

    # FICHAS DEL NPC
    fichas_rival = interfase.fichas_cpu()

    # MODIFICADORES CORRESPONDIENTES A CADA CASILLA ESPECIAL
    botones_indieces = interfase.indice_modificadores()

    # BOTONES TABLERO
    tablero = interfase.tablero()

    # MARCADORES DE TIEMPO Y PUNTAJE
    puntaje_y_tiempo = interfase.marcadore_puntaje_tiempo()

    # LAYOUT CON LA CARGA GENERAL DE LA VENTANA
    layout = interfase.layout_general(fichas_rival, opciones_de_inicio,
                                      tablero, puntaje_y_tiempo,
                                      botones_indieces, fichas,
                                      opciones_de_juego)

    # SE GENERA LA VENTANA
    window = sg.Window('SCRABBLE AR', layout, default_button_element_size=(
        2, 2), finalize=True, resizable=True,  auto_size_buttons=True)

    # METODO PARA PINTAR EL TABLERO PARA LA PRESENTACION
    funciones.dibujo_python(window)

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
    lugares_no_disponibles = []  # lleva la cuenta de los lugares que ya
    # escribi para despintar la casilla
    # anterior cuando toco una nueva
    ant = ()
    lugar = ()                    # marca la casilla actual
    layout2 = layout              # esto no se que es
    # cantidad de veces de pedidos para hacer el cambio de fichas totales
    cantidad_de_veces_Repartidas = 0
    timer_running, counter = False, 0  # seteos para el timer,
    dificult = ''     # la dificultad actual que luego sera asignada
    h = False
    v = False
    turno = ''
    tiempo_limite = 0
    start_time = int(round(time.time() * 100))

    while True:
        event, values = window.read(timeout=0)
        print(total_letras)
        # print(counter)
        if event in (None, 'Salir'):
            break
        else:
            if total_letras == 0:
               sg.popup('No hay mas letras en la bolsa') 
               funciones.analizar_ganador(puntos_jugador_total,puntos_npc_total)

            if total_letras <= 7 or cantidad_de_veces_Repartidas > 3 :   
                window['Repartir De Nuevo'].update(disabled=True) 

            if cantidad_de_veces_Repartidas == 3:   
                window['Terminar partida'].update(disabled=False)
                sg.popup('NO puedes repartir de nuevo otra vez! ',
                'En caso de no tener palabras posibles ahora puedes terminar la partida')
                # este aumento de la variable es para que no entre mas aca
                cantidad_de_veces_Repartidas+=1

            if event == "Terminar partida":
                sg.popup('ok terminaste la partida, vamos a analizar el ganador')
                funciones.analizar_ganador(puntos_jugador_total,puntos_npc_total)    

            if turno == 'player_2':
                puntos_npc, turno, total_letras = ia.turno_maquina(window,
                                                                   letras_atril_rival,
                                                                   lugar,
                                                                   lugares_no_disponibles,
                                                                   turno, bolsa_total,
                                                                   letras_usadas_en_tablero,
                                                                   dificult, l2_guar, total_letras)
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
                    funciones.volver_a_pintar_la_casilla(
                        lugar, window, dificult)
                ant = lugar

            # si el evento seria una letra y lugar tiene algo es xq marque algo
            if event in ("Boton_1", "Boton_1", "Boton_2", "Boton_3", "Boton_4",
                         "Boton_5", "Boton_6", "Boton_7") and lugar:
                letra = window[event].GetText()  # asigno la letra del evento
                if lugar not in lugares_no_disponibles:  # si el lugar no lo
                    # use vemos si es la primera letra, seteamos la orientacion
                    if len(letras_usadas_en_tablero) == 0:
                        funciones.letra_al_tablero(window,
                                                   letras_usadas_en_tablero,
                                                   botones_usados,
                                                   letras_atril_jugador,
                                                   lugares_no_disponibles,
                                                   letra, event, lugar)

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
                        if h:
                            funciones.letra_al_tablero(window,
                                                       letras_usadas_en_tablero,
                                                       botones_usados,
                                                       letras_atril_jugador,
                                                       lugares_no_disponibles,
                                                       letra,
                                                       event, lugar)
                        elif v:
                            funciones.letra_al_tablero(window,
                                                       letras_usadas_en_tablero,
                                                       botones_usados,
                                                       letras_atril_jugador,
                                                       lugares_no_disponibles,
                                                       letra,
                                                       event, lugar)
                        else:
                            sg.popup('lugar invalido')

                        # hay que declarar una variable dific para enviar en
                        # lugar de facil
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
                    cantidad_de_veces_Repartidas, total_letras = funciones.repartir_fichas_de_nuevo(
                        window, cantidad_de_veces_Repartidas,
                        letras_atril_jugador,
                        bolsa_total, total_letras)
                    turno= 'player_2'   
                else:
                    sg.Popup(
                        'Estas en medio de una mano, tenes q tener 7 fichas ',
                        ' para cambiar')
            # quita elementos del tablero, desde el ultimo al primero
            elif event == "Borrar":
                if puntos_jugador != 0:
                    puntos_jugador -= funciones.puntos_de_letra(letras_usadas_en_tablero[len(
                        letras_usadas_en_tablero)-1], dificult,
                        lugares_no_disponibles[len(lugares_no_disponibles)-1])
                    window["puntaje_de_jugada"].update(puntos_jugador)
                    funciones.quitar_fichas(window, letras_usadas_en_tablero,
                                            botones_usados,
                                            lugares_no_disponibles,
                                            letras_atril_jugador, dificult)

            # para inicializar el juego
            elif event == "Comenzar":
                start_time = int(round(time.time() * 100))
                counter = int(round(time.time() * 100)) - start_time
                nombre = funciones.carga_nombre()
                interfase.tablero_default(window)
                if total_letras >= 14:
                    timer_running, dificult, tiempo_limite, total_letras = funciones.cargar_juego(
                        window, values, timer_running, nombre, bolsa_total, letras_atril_jugador, letras_atril_rival, total_letras)
                else:
                    sg.popup(
                        "La cantidad de letras registras es invalida,configure el juego nuevamente")
                    sys.exit()
                print('tiempo_limite', tiempo_limite)
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
                interfase.tablero_default(window)
                if os.path.isfile('./texto/save.json'):
                    counter, dificult, puntos_jugador, puntos_jugador_total, puntos_npc, puntos_npc_total, h, v = funciones.cargar_partida(
                        window, letras_atril_jugador, botones_usados, lugares_no_disponibles, l2_guar, letras_atril_rival)
                    timer_running = not timer_running
                else:
                    sg.popup('No tenes partidas guardadas')

            elif event == "Configuracion":
                funciones.configuracion_de_juego()

            elif event == "TOP":
               ranking.ranking()

            # esto es para que corra el tiempo
            elif timer_running:
                # window['-OUTPUT-'].update(
                # '{:02d}:{:02d}'.format((counter//100)
                # // 60, (counter // 100) % 60, counter % 100))

                window['-OUTPUT-'].update('{:02d}:{:02d}'.format(
                    (counter // 500) // 60, (counter // 500) % 60, counter % 500))
                counter += 1

                # 6000 equivale a 1 minuto, 60000 a 10 minutos
                if counter == tiempo_limite:
                    timer_running = not timer_running
                    sg.Popup('termino el tiempo,analizando ganador:')
                    funciones.analizar_ganador(puntos_jugador_total,puntos_npc_total)

            # aca va evaluar,evalua la palabra y resetea las orientaciones
            if event == "Evaluar":

                palabra_final = "".join(letras_usadas_en_tablero)
                v = False
                h = False
                if funciones.verificar_palabra(palabra_final) and len(palabra_final) > 1:
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
                    total_letras = funciones.pedir_fichas(
                        window, botones_usados, letras_atril_jugador,
                        bolsa_total, total_letras)
                    turno = 'player_2'
                else:
                    print("palabra invalida")
                    for i in range(len(letras_usadas_en_tablero)):
                        funciones.quitar_fichas(
                            window, letras_usadas_en_tablero, botones_usados,
                            lugares_no_disponibles, letras_atril_jugador,
                            dificult)
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
                                        "dificultad": dificult, "hor": h,
                                        "ver": v}
                        dic['tiempo'] = {'reloj': counter}
                        json.dump(dic, j, indent=4)
                else:
                    sg.Popup(
                        "Solo se puede guardar una partida teniendo",
                        "el atril completo")
        window.Refresh()
    window.close()


if __name__ == "__main__":
    iniciar_juego()
