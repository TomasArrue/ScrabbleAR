from funciones import funciones, ia, interfase, ranking, configuracion
dic = {}

def cargar_letra_1(window,letras_usadas_en_tablero,botones_usados,
                letras_atril_jugador,lugares_no_disponibles,letra,event,
                lugar,puntos_jugador):
    """
        carga la primer letra de la palabra en el tablero
    """
    funciones.letra_al_tablero(window,letras_usadas_en_tablero,botones_usados,
                                letras_atril_jugador,lugares_no_disponibles,
                                letra, event, lugar)

    # hay que declarar una variable dific para enviar
    # en lugar de facil
    puntos_jugador += funciones.puntos_de_letra(letra, dificult,
                                                             lugar)
    window["puntaje_de_jugada"].update(puntos_jugador)
    # vemos si es la primera letra, seteamos la orientacion de
    # la palabra


def cargar_letra_2(window,letras_usadas_en_tablero,botones_usados,
                    letras_atril_jugador,lugares_no_disponibles,letra,event,
                    lugar,puntos_jugador):
    """
        carga la segunda letra y determi a si es horzontal o vertical
    """
    h = funciones.horizontal(lugar, lugares_no_disponibles
                            [len(lugares_no_disponibles)-1])
    v = funciones.vertical(lugar, lugares_no_disponibles
                            [len(lugares_no_disponibles)-1])
    if h:funciones.letra_al_tablero(window,letras_usadas_en_tablero,
                                    botones_usados,letras_atril_jugador,
                                    lugares_no_disponibles,letra,event, lugar)
    elif v:funciones.letra_al_tablero(window,letras_usadas_en_tablero,
                                        botones_usados,letras_atril_jugador,
                                        lugares_no_disponibles,letra,event,
                                        lugar)
    else:sg.popup('lugar invalido')

    # hay que declarar una variable dific para enviar en
    # lugar de facil
    puntos_jugador += funciones.puntos_de_letra(letra, dificult, lugar)
    window["puntaje_de_jugada"].update(puntos_jugador)


def cargar_letra_3(window,letras_usadas_en_tablero,botones_usados,
                    letras_atril_jugador,lugares_no_disponibles,letra,event,
                    lugar,puntos_jugador):
    if funciones.horizontal(lugar, lugares_no_disponibles
                            [len(lugares_no_disponibles)-1]) and h:
        funciones.letra_al_tablero(window,letras_usadas_en_tablero,
                                    botones_usados,letras_atril_jugador,
                                    lugares_no_disponibles,letra, event,lugar)

        puntos_jugador += funciones.puntos_de_letra(letra, dificult, lugar)
        window["puntaje_de_jugada"].update(puntos_jugador)
    elif funciones.vertical(lugar, lugares_no_disponibles
                            [len(lugares_no_disponibles)-1]) and v:
        funciones.letra_al_tablero(window,letras_usadas_en_tablero,
                                    botones_usados,letras_atril_jugador,
                                    lugares_no_disponibles,letra, event, lugar)

        puntos_jugador += funciones.puntos_de_letra(letra, dificult, lugar)
        window["puntaje_de_jugada"].update(puntos_jugador)
    else:
        sg.Popup('Lugar Invalido')


dic[0] = cargar_letra_1(window,letras_usadas_en_tablero,botones_usados,
                letras_atril_jugador,lugares_no_disponibles,letra,event,
                lugar,puntos_jugador)



dic[1] = cargar_letra_2(window,letras_usadas_en_tablero,botones_usados,
                    letras_atril_jugador,lugares_no_disponibles,letra,event,
                    lugar,puntos_jugador)



dic[2] = cargar_letra_3(window,letras_usadas_en_tablero,botones_usados,
                    letras_atril_jugador,lugares_no_disponibles,letra,event,
                    lugar,puntos_jugador)


###############################################################################
