import sys
import os
# usamos el import sys para abortar el programa en caso de que los  archivos no
# esten disponibles para ejecutar
import random
import json
import PySimpleGUI as sg
from funciones import funciones, ia, interfase, ranking, configuracion
import time
from datetime import date


def test_de_archivo():
    '''
        solo para testear si se encuentra el config.json con todos los datos
        necesarios para que corra el juego, en caso que no se encuentre
        se aborta el programa y se informa de la falta del archivo
    '''
    return os.path.isfile('./texto/config.json') and (
           os.path.isfile('./texto/config_default.json')) and (
           os.path.isfile('./texto/dibujo.json')) and (
           os.path.isfile('./texto/ranking.json'))
        

def iniciar_juego():

    # INICIA EL PROGRAMA PRINCIPAL

    test_de_archivo()

    bolsa_total = funciones.crear_bolsita_total()
    total_letras = 0
    for k, v in bolsa_total.items():
        total_letras += v

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

    pista = interfase.opciones_pista()

    # LAYOUT CON LA CARGA GENERAL DE LA VENTANA
    layout = interfase.layout_general(fichas_rival, opciones_de_inicio,
                                      tablero, puntaje_y_tiempo,
                                      botones_indieces, fichas,
                                      opciones_de_juego, pista)

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
    lugar = ()       # marca la casilla actual
    # cantidad de veces de pedidos para hacer el cambio de fichas totales
    cantidad_de_veces_Repartidas = 0
    cantidad_de_veces_Repartidas_IA = 0
    timer_running, counter = False, 0  # seteos para el timer,
    dificult = ''     # la dificultad actual que luego sera asignada
    h = False
    v = False
    turno = ''
    nombre = ''
    tiempo_limite = 0
    start_time = int(round(time.time() * 100))
    disponibles = True  # variable para saber si la maquina tiene palabras disp
    contador_pistas = 0

    while True:
        event, values = window.read(timeout=10)
      
        if event in (None, 'Salir'):
            break
        else:

            if total_letras < 1:
                sg.popup('No hay mas letras en la bolsa')
                funciones.analizar_ganador(puntos_jugador_total,
                                           puntos_npc_total, nombre, dificult)
            
            if cantidad_de_veces_Repartidas == 3:
                window['Repartir De Nuevo'].update(disabled=True)
                window['Terminar partida'].update(disabled=False)
                sg.popup('NO puedes repartir de nuevo otra vez! ',
                         'En caso de no tener palabras posibles ahora puedes',
                         ' terminar la partida')
                # este aumento de la variable es para que no entre mas aca
                cantidad_de_veces_Repartidas += 1

            if event == "Terminar partida":
                sg.popup('ok terminaste la partida, vamos a analizar el ganador')
                funciones.analizar_ganador(puntos_jugador_total,
                                           puntos_npc_total, nombre, dificult)

            if turno == 'player_2':
                if disponibles:
                    print(total_letras)
                    puntos_npc, turno, total_letras, disponibles, cantidad_de_veces_Repartidas_IA = ia.turno_maquina(window,
                                                                                    letras_atril_rival,
                                                                                    lugar,
                                                                                    lugares_no_disponibles,
                                                                                    turno, bolsa_total,
                                                                                    letras_usadas_en_tablero,
                                                                                    dificult, l2_guar, total_letras,
                                                                                    disponibles, 
                                                                                    cantidad_de_veces_Repartidas_IA)
                    puntos_npc_total = puntos_npc_total+puntos_npc
                    window["puntaje_PC"].update(puntos_npc_total)
                else:
                    sg.popup('la maquina no puede jugar mas!')
                    turno = 'player_1'
                print('turno vuelta', turno)
                if (dificult == 'Dificil'): 
                    # si es difiultad dificil solo se podra usar 3 veces las pistas
                    if (contador_pistas < 3): 
                        window['boton_pista'].update(disabled=False)
                else: 
                    # si es dificultad media se podra usar hasta 6 veces
                    if (contador_pistas < 6): 
                        window['boton_pista'].update(disabled=False)
                sg.Popup('Tu Turno!')

            if type(event) is tuple:
                lugar = event
                # pinto el lugar que estoy seleccionando,hago esa pregunta para
                # que no trate  de marcar un casillero que ya tiene una letra
                if lugar not in lugares_no_disponibles:
                    window[lugar].update(button_color=('white', 'darkgrey'))
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
                    # la palabra
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
                if not botones_usados and cantidad_de_veces_Repartidas < 3:
                    cantidad_de_veces_Repartidas, total_letras = funciones.repartir_fichas_de_nuevo(
                        window, cantidad_de_veces_Repartidas,
                        letras_atril_jugador,
                        bolsa_total, total_letras)
                    turno = 'player_2'
                elif cantidad_de_veces_Repartidas >= 3:
                    sg.Popup('Ya hiciste el maximo de cambios de mano')
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
                        window, values, timer_running, nombre, bolsa_total,
                        letras_atril_jugador, letras_atril_rival, total_letras)
                else:
                    sg.popup(
                        'La cantidad de letras registras es invalida,',
                        ' configure el juego nuevamente')
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
                    dic = funciones.cargar_partida(window, letras_atril_jugador,
                                                   botones_usados,
                                                   lugares_no_disponibles,
                                                   l2_guar, letras_atril_rival)
                    counter = dic['tiempo']['reloj']
                    dificult = dic["otros"]["dificultad"]
                    puntos_jugador = dic["puntos"]["puntos_jugador"]
                    puntos_jugador_total = dic["puntos"]["puntos_jugador_total"]
                    puntos_npc = dic["puntos"]["puntos_npc"]
                    puntos_npc_total = dic["puntos"]["puntos_npc_total"]
                    h = dic["otros"]["hor"]
                    v = dic["otros"]["ver"]
                    tiempo_limite = dic["tiempo"]["fin"]
                    contador_pistas = dic["otros"]["contador_pistas"]
                    cantidad_de_veces_Repartidas = dic["otros"]["cantidad_de_veces_Repartidas"]
                    cantidad_de_veces_Repartidas_IA = dic["otros"]["cantidad_de_veces_Repartidas_IA"]
                    timer_running = not timer_running

                else:
                    sg.popup('No tenes partidas guardadas')

            elif event == "Configuracion":
                configuracion.configuracion_de_juego()

            elif event == "TOP":
                ranking.ranking()

            # se podra usar la pista una vez por turno en nivel medio
            elif event == 'boton_pista':
                lista=ia.buscar_palabras_rival(letras_atril_jugador,dificult)
                window['boton_pista'].update(disabled=True) 
                contador_pistas += 1
                if (len(lista))>0:
                  print(dificult)    
                  if dificult == 'Dificil':
                    sg.popup('Una Palabra podria ser: ',random.choice(lista)) 
                  else:   
                    sg.popup('Con las letras que tienes puedes formar palabras! :D')
                else:  
                  sg.popup('Con las letras que tienes NO puedes formar palabras! :(')  

            # esto es para que corra el tiempo
            elif timer_running:
                window['-OUTPUT-'].update('{:02d}:{:02d}'.format(
                    (counter // 60) // 60, (counter // 60) % 60))
                counter += 1

                # 6000 equivale a 1 minuto, 60000 a 10 minutos

                if counter == tiempo_limite:
                    timer_running = not timer_running
                    sg.Popup('termino el tiempo,analizando ganador:')
                    funciones.analizar_ganador(puntos_jugador_total,
                                               puntos_npc_total, nombre,
                                               dificult)

            # aca va evaluar,evalua la palabra y resetea las orientaciones
            if event == "Evaluar":
                print(puntos_jugador_total)
                print(type(puntos_jugador_total))
                palabra_final = "".join(letras_usadas_en_tablero)
                v = False
                h = False
                if  len(palabra_final) > 1 and funciones.verificar_palabra(palabra_final, dificult) :
                    lista_coords = []
                    tamanio_pal = len(palabra_final)
                    for i in range(1, tamanio_pal+1):
                        element = lugares_no_disponibles[-i]
                        lista_coords.append(element)
                    lista_coords.reverse()
                    puntos_jugador_total_aux = funciones.puntos_de_palabra(
                        dificult, lista_coords, puntos_jugador)
                    puntos_jugador_total += puntos_jugador_total_aux
                    window["puntaje_propio"].update(puntos_jugador_total)
                    l2_guar.extend(letras_usadas_en_tablero)
                    puntos_jugador = 0
                    window["puntaje_de_jugada"].update("0")
                    if len(letras_usadas_en_tablero) <= total_letras:
                        total_letras = funciones.pedir_fichas(
                            window, botones_usados, letras_atril_jugador,
                            bolsa_total, total_letras)
                    else:
                        sg.popup('No se pueden reponer las fichas porque no',
                                 ' hay suficiente en la bolsa')
                    letras_usadas_en_tablero.clear()
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
                                        "ver": v,"contador_pistas":contador_pistas,
                                        "cantidad_de_veces_Repartidas":cantidad_de_veces_Repartidas,
                                        "cantidad_de_veces_Repartidas_IA":cantidad_de_veces_Repartidas_IA}
                        dic['tiempo'] = {'reloj': counter, 'fin': tiempo_limite}
                        cantidad_de_veces_Repartidas_IA
                        json.dump(dic, j, indent=4)
                        sg.Popup("Partida Guardada")
                else:
                    sg.Popup(
                        "Solo se puede guardar una partida teniendo",
                        "el atril completo")
        window.Refresh()
    window.close()


if __name__ == "__main__":
    if test_de_archivo():
        iniciar_juego()
    else:
        sg.Popup('ERROR ---> Archivo/s no encontrado/s')
        sys.exit()
