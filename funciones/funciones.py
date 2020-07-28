import json
import PySimpleGUI as sg
import random
from pattern.text.es import lexicon, spelling, verbs
from itertools import permutations


def configuracion_de_juego():
    """
        configuracion del juego inicial,cargamos el config.json, para poder
        cambiar la cantidades de letras iniciales en la bolsa de fichas y
        ademas podemos editar el valor de cada ficha
    """
    with open('./texto/config.json', 'r') as cf:
        c = json.load(cf)

    diccionario_cantidad_de_letras = c['cantidad_de_letras']
    diccionario_cantidad_de_puntos = c['valor_por_letra']

    layout3 = [
        [sg.Text("Configuracion", size=(10, 1), justification='left',font=("Chalkboard", 25), relief=sg.RELIEF_RIDGE)],
        [sg.Text(k, size=(3, 1), justification='center') for k, v in diccionario_cantidad_de_letras.items()],
        [sg.Text('PARA MODIFICAR LA CANTIDAD DE LETRAS POR LETRA CAMBIE EL VALOR A LA LETRA CORRESPONDIENTE :')],
        [sg.Input(v, size=(3, 1), key=(k+'_cant')) for k, v in diccionario_cantidad_de_letras.items()],
        [sg.Text('PARA MODIFICAR EL VALOR DE LAS LETRAS POR LETRA CAMBIE EL VALOR A LA LETRA CORRESPONDIENTE:')],
        [sg.Input(v, size=(3, 1), key=(k+'_valor')) for k, v in diccionario_cantidad_de_puntos.items()],
        [sg.Text('')],[sg.Text('PARA MODIFICAR EL TIEMPO INGRESE EL TIEMPO EN MINUTOS (de 5 a 30) QUE QUIERES QUE DURE LA PARTIDA')],
        [sg.Input(size=(9, 1), key=('time'))],
        [sg.Button('CONFIGURACION POR DEFECTO'), sg.Button('GUARDAR CONFIGURACION'), sg.Button('CANCELAR')]
    ]

    window3 = sg.Window('Configuracion').Layout(layout3)
    print('tests')
    while True:

        event3, values3 = window3.Read()

        if event3 == 'CANCELAR' or event3 == None:
            break

        if event3 == 'CONFIGURACION POR DEFECTO':
            with open('./texto/config_default.json', 'r') as cf:
                c = json.load(cf)
            with open('./texto/config.json', 'w') as cf:
                json.dump(c,cf, indent=4)    
            sg.popup('Se restauro la configuracion inicial :D')    
            break


        if event3 == 'GUARDAR CONFIGURACION':
            # with open('config.json','w') as cf:
            try:
                num_tiempo = int(values3['time'])
                if (num_tiempo > 30):
                    num_tiempo = 30
                if (num_tiempo < 5):
                    num_tiempo = 5
            except (ValueError):
                # seteamos 10 minutos en caso de cargar erronea de tiempo
                num_tiempo = 10
                sg.Popup('El tiempo se cargo de maneara erronea, pero ',
                         'cargamos la partida de 10 minutos')
            
            for k, v in diccionario_cantidad_de_letras.items():

                try:
                    diccionario_cantidad_de_letras[k]= int(values3[k+'_cant'])
                except (ValueError):
                    diccionario_cantidad_de_letras[k] = 1
                try:
                    diccionario_cantidad_de_puntos[k]= int(values3[k+'_valor'])
                except (ValueError):
                    diccionario_cantidad_de_puntos[k] = 1    

            with open('./texto/config.json', 'w') as cf:
                c['cantidad_de_letras']=diccionario_cantidad_de_letras 
                c['valor_por_letra']=diccionario_cantidad_de_puntos 
                c['tiempo']= num_tiempo   
                json.dump(c,cf, indent=4)   
                
            sg.Popup('La duracion de la partida sera de: ',num_tiempo, ' minutos')
            sg.popup('Se configuro la partida')
            break              

    window3.close()


def crear_bolsita_total():
    """
        Generamos la bolsas con las fichas totales para usar en el juego,
        las cuales tenemos almacenadas en el config.json
    """
    with open('./texto/config.json', 'r') as cf:
        c = json.load(cf)
    bolsa = c['cantidad_de_letras']

    return bolsa


def crear_atril(bolsa_total):
    """
        Toma las letras de a una desde el archivo configuracion
    """
    letra = random.choice(list(bolsa_total.keys()))
    while bolsa_total[letra] == 0:
        letra = random.choice(list(bolsa_total.keys()))
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
        [sg.Input('', key='name')],
        [sg.Button('Listo')]
    ]
    window3 = sg.Window('Ingresa datos', layout3)
    while True:
        event, values = window3.read()
        if event == 'Listo':
            nombre = values['name']
            break
    window3.close()

    return nombre


def asignar_colores_al_tablero(window, dificultad):
    """
       Se van a pintar los botones de la matriz que conforman el tablero
       segun las coordenas que vengan en el archivo json, dependiendo
       el nivel que hayamos elegido
    """
    with open('./texto/config.json', 'r') as t:
        dic = json.load(t)

    # print(dificultad)
    tablero_config = dic[dificultad]

    for colores in tablero_config.keys():
        lista_de_cord = tablero_config[colores]
        for par_de_cord in lista_de_cord:
            x, y = par_de_cord
            window[x, y].update(button_color=(colores, colores))


def cargar_juego(window, values, timer_running, nombre, bolsa_total,
                 letras_atril_jugador, letras_atril_rival):
    """
        iniciamos todo el seteo inicial del juego:
            -la dificultad segun la seleccionada en el menu
            -Pintamos el tablero segun la dificultad
            -Ocultamos los botones de Comenzar, Cargar Partida
            -Volvemos visibles los botones de Guardar, Salir
            -Volvemos visibles las opciones de juego para poder jugar
    """
    very_dificult = values['dificultad']
    asignar_colores_al_tablero(window, very_dificult)
    window['opcionesJuego'].update(visible=True)
    window['Comenzar'].update(visible=False)
    window['Configuracion'].update(visible=False)
    window['Cargar Partida'].update(visible=False)
    window['Guardar Partida'].update(visible=True)
    window['Salir'].update(visible=True)
    texto = nombre.upper()+' TU PUNTAJE ES:'
    window['tu_puntaje_propio'].update(texto)
    window['puntaje'].update(visible=True)
    window['indice'].update(visible=True)
    window['atrilFichasRival'].update(visible=True)
    window['atrilFichas'].update(visible=True)
    window['dificultad'].update(visible=False)

    for i in range(7):  # carga de las 7 fichas al inicio

        nro_de_boton = 'Boton_'+str(i+1)
        obtener_fichas(window, nro_de_boton, letras_atril_jugador, bolsa_total)
        # generamos las fichas del rival tambien
        letra_rival = crear_atril(bolsa_total)
        letras_atril_rival.append(letra_rival)  # Las agregamos a su lista

    timer_running = not timer_running

    return timer_running, very_dificult


def cargar_partida(window, letras_atril_jugador, botones_usados,
                   lugares_no_disponibles, letras_guardadas, letras_atril_rival):
    """
       asdasd
    """
    try:
        with open('./texto/save.json', 'r') as archivo_carga:
            dic = json.load(archivo_carga)
    except FileNotFoundError:  
        sg.popup('No se encontro el archivo de la partida guardad')      
        return 'Error'
    asignar_colores_al_tablero(window, dic["otros"]["dificultad"])
    window['opcionesJuego'].update(visible=True)
    window['Comenzar'].update(visible=False)
    window['Configuracion'].update(visible=False)
    window['Cargar Partida'].update(visible=False)
    window['Guardar Partida'].update(visible=True)
    window['Salir'].update(visible=True)
    
    texto=dic['nombre'].upper()+' TU PUNTAJE ES:'
    window['tu_puntaje_propio'].update(texto)
    
    window['puntaje_propio'].update("PUNTAJE DE {0} ES :0".format("pepe"))
    window['puntaje'].update(visible=True)
    window["puntaje_propio"].update(dic["puntos"]["puntos_jugador_total"])
    window["puntaje_PC"].update(dic["puntos"]["puntos_npc_total"])
    window['indice'].update(visible=True)
    window['atrilFichasRival'].update(visible=True)
    window['atrilFichas'].update(visible=True)
    window['dificultad'].update(visible=False)

    window['-OUTPUT-'].update('{:02d}:{:02d}'.format(
        (dic['tiempo']['reloj'] // 100) // 60, (dic['tiempo']['reloj'] // 100) % 60))

    for letra in dic["otros"]["letras_usadas"]:
        letras_guardadas.append(letra)

    # carga de las 7 fichas al inicio
    for i in range(len(dic["atril"]["atril_jugador"])):

        nro_de_boton = 'Boton_'+str(i+1)
        window[nro_de_boton].update(dic["atril"]["atril_jugador"][i])
        letras_atril_jugador.append(dic["atril"]["atril_jugador"][i])

    letras_atril_rival.extend(dic["atril_rival"]["letras_atril_rival"])

    letras_atril_jugador.append(dic["atril"]["atril_jugador"][i])
    for i in range(len(dic["otros"]["lugares"])):
        lugares_no_disponibles.append(tuple(dic["otros"]["lugares"][i]))
        window[lugares_no_disponibles[i]].update(
            dic["otros"]["letras_usadas"][i],
            button_color=('black', 'oldlace'))

    return dic['tiempo']['reloj'], dic["otros"]["dificultad"], dic["puntos"]["puntos_jugador"], dic["puntos"]["puntos_jugador_total"], dic["puntos"]["puntos_npc"], dic["puntos"]["puntos_npc_total"], dic["otros"]["hor"], dic["otros"]["ver"]


def volver_a_pintar_la_casilla(cord, window, dificult):
    """
        este modulo nos sirve para volver a pintar un boton de su color inicial
        en caso de que tengamos que sacar una ficha que pusimos
    """
    with open('./texto/config.json', 'r') as p:
        dicc = json.load(p)
    # la dific tiene que vernir como parametro para saber que tablero abrir
    tablero_actual = dicc[dificult]

    if list(cord) in tablero_actual["indianred"]:
        window[cord].update(button_color=('indianred', 'indianred'))
    elif list(cord) in tablero_actual["goldenrod"]:
        window[cord].update(button_color=('goldenrod', 'goldenrod'))
    elif list(cord) in tablero_actual["mediumseagreen"]:
        window[cord].update(button_color=('mediumseagreen', 'mediumseagreen'))
    elif list(cord) in tablero_actual["skyblue"]:
        window[cord].update(button_color=('skyblue', 'skyblue'))
    else:
        window[cord].update(button_color=('grey', 'white'))


def verificar_palabra(palabra):
    """
        verificamos si la palabra es valida
    """
    print(palabra)
    # if palabra in verbs or ((palabra in lexicon) and (palabra in spelling)):
    if palabra in lexicon and spelling or palabra in verbs:
        return(True)
    else:
        return(False)  # cambiar a false


def obtener_fichas(window, nro_de_boton, letras_atril_jugador, bolsa_total):
    """
        Este metodo nos da una ficha "nueva".
        Generamos una letra random la agregamos a la lista de letras de
        nuestro atril, luego con la key del boton recibida como parametro
        actualizamos el valor del boton con la nueva letra
    """
    letra = crear_atril(bolsa_total)
    letras_atril_jugador.append(letra)
    window[nro_de_boton].update(letra)
    window[nro_de_boton].update(button_color=('black', 'oldlace'))
    window.Refresh()


def repartir_fichas_de_nuevo(window, cantidad_de_veces_Repartidas,
                             letras_atril_jugador, bolsa_total):
    """
        Utilizamos este metodo para poder cambiar la mano de fichas que
        tenemos, y tenemos permitido hacerlo hasta 3 veces
    """
    letras_atril_jugador.clear()
    if (cantidad_de_veces_Repartidas < 3):
        cantidad_de_veces_Repartidas = cantidad_de_veces_Repartidas+1
        for i in range(7):  # carga de las 7 fichas
            nro_de_boton = 'Boton_'+str(i+1)
            obtener_fichas(window, nro_de_boton,
                           letras_atril_jugador, bolsa_total)
    else:
        sg.Popup('Ya hiciste el maximo de cambios de mano')

    return cantidad_de_veces_Repartidas


def quitar_fichas(window, usados, botones_usados, no_disponibles,
                  letras_atril_jugador, dificult):
    """
        quitar fichas nos permite sacar las fichas ingresadas al tablero en el
        turno correspondiente.
        Mientras que la longitud lista de usados del turno sea mayor a 0 vamos
        a poder retirar fichas que ingresamos, en caso de que no se pueda no
        podremos quitar mas
    """
    # print(len(usados),' ',len(no_disponibles),' ',len(botones_usados))
    # Aca antes de borrar una letra vamos a preguntar si hay letras para borrar
    # en caso contrario no podras borrar mas letras
    if len(usados) > 0:
        # Saca la ultima letra de la palabra cargada - el pop saca de usados
        # el elemento de la ultima posicion de la lista de usados
        letra_a_borrar = usados.pop()
        boton_a_recuperar = botones_usados.pop()
        # vuelve a cargar la letra que sacamos del tablero en el atril de
        # nuestras fichas
        letras_atril_jugador.append(letra_a_borrar)
        # Saca la ultima coordenada de la palabra cargada - el pop saca de
        # no_disponibles el elemento de la ultima posicion de la lista
        # de no_disponibles
        coord_a_liberar = no_disponibles.pop()
        # vuelve a pintar la casilla de su color en estado inicial
        volver_a_pintar_la_casilla(coord_a_liberar, window, dificult)
        window[coord_a_liberar].update("")
        window[boton_a_recuperar].update(
            button_color=('black', 'oldlace'), disabled=False)
    else:
        sg.Popup('No hay fichas para borrar')


def pedir_fichas(window, botones_usados, letras_atril_jugador, bolsa_total):
    """
       El pedir fichas nos permite pedir la cantidad de fichas usadas en el
       ultimo turno hasta llegar a tener 7 nuevamente.
    """
    for i in botones_usados:
        letra = letras_atril_jugador[len(letras_atril_jugador)-1]
        window[i].update(letra, disabled=False)
        obtener_fichas(window, i, letras_atril_jugador, bolsa_total)
    for i in range(len(botones_usados)):
        botones_usados.pop()


def letra_al_tablero(window, usados, botones_usados, letras_atril_jugador,
                     no_disponibles, letra, event, lugar):
    """
       Utilizamos este metodo para graficar el colocar la ficha en el tablero.
       -Guardamos la ficha en una lista de "usados"
       -Guardamos el nombre del boton para luego recuperarlo
       -En el tablero ponemos el valor de la ficha seleccionada
       -Sacamos la letra de nuestro atril, y la deshabilitamos del atril
       -Para finalizar guardamos las coordenadas del lugar en una lista de
        lugares no disponibles
    """
    usados.append(letra)
    botones_usados.append(event)
    window[lugar].update(letra, button_color=('black', 'oldlace'))
    letras_atril_jugador.remove(letra)
    window[event].update(button_color=('darkgrey', 'darkgrey'), disabled=True)
    no_disponibles.append(lugar)


def puntos_de_letra(letra, dificultad, coord):
    """
       calculamos el valor de la letra ingresada en el tablero. accedemos al
       json para ver su puntaje asociado
    """
    with open('./texto/config.json', 'r') as p:
        dicc = json.load(p)
    valor_de_letra = dicc["valor_por_letra"]
    tablero_actual = dicc[dificultad]
    letra = letra.upper()
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


def puntos_de_palabra(dificultad, no_disponibles, puntos):
    """
       En esta parte vamos a calcular el total de los puntos de la palabra
       cargada.
       Segun la dificultad vamos a tener distintos modificadores en cada color
       Si nuestra palabra pasa por casillas con colores el puntaje final se
       vera afectado
    """
    with open('./texto/config.json', 'r') as p:
        dicc = json.load(p)
    tablero_actual = dicc[dificultad]
    # print('puntos..',puntos)
    # conjuntos para hacer la interseccion
    green = set(map(tuple, tablero_actual["mediumseagreen"]))
    blue = set(map(tuple, tablero_actual["skyblue"]))

    int_green = green.intersection(set(no_disponibles))
    int_blue = blue.intersection(set(no_disponibles))
    # print('cordenas verdes..',int_green)
    # print('cordenas no disponibles..',no_disponibles)

    for element in int_green:
        num = random.randint(0, 10)
        puntos = puntos - num
        # print("num aleatorio...", num)
    for element in int_blue:
        puntos = puntos // 2
    print('puntos 2..', puntos)
    return puntos


def formet(d):
    lista = []
    for k, v in d.items():
        variable = '{} {} '.format("Jugador:", k) + '{} {} '.format(
            "Puntaje:", v["Puntos"]) + '{} {}'.format("Fecha:", v["Fecha"])
        lista.append(variable)
    return lista


def vertical(pos_actual, pos_anterior):

    if pos_anterior[0]+1 == pos_actual[0] and pos_actual[1] == pos_anterior[1]:
        return True
    else:
        return False


def horizontal(pos_actual, pos_anterior):

    if pos_anterior[0] == pos_actual[0] and pos_actual[1] == pos_anterior[1]+1:
        return True
    else:
        return False


# ============================= IA =============================


def validar_palabra(permutaciones, permutaciones_validas):
    """
        Valida palabras que esten dentro de las permutaciones
        pasadas por parametro y las agrega a una lista de palabras
        validas
    """
    for pal in permutaciones:
        if pal in lexicon and spelling or pal in verbs:
            # if pal in verbs or ((pal in lexicon) and (pal in spelling)):
            # si la palabra es valida va a la lista de permutaciones
            permutaciones_validas.append(pal)
    return permutaciones_validas


def buscar_palabras_rival(letras_atril_rival):
    """
        recibe el las fichas del atril del rival y genera una lista de
        palabras validas
    """
    # lista vacia para guardar las permutaciones validas
    permutaciones_validas = []
    for i in range(len(letras_atril_rival)):
        # este if es para empezar a armar permutaciones de al menos dos
        #  caracteres generamos permutaciones con i+1 caracteres
        if (i+1 >= 2):
            permutaciones_temp = {
                "".join(p) for p in permutations(letras_atril_rival, i+1)}
            # vemos cuales de esas permutaciones son validas, y las vamos
            # guardando en una lista
            validar_palabra(permutaciones_temp, permutaciones_validas)
    return permutaciones_validas


def todas_los_posiciones_validas(tamanio_pal, lugar, lugar_aux,
                                 lugares_no_disponibles, orientacion):
    """
        Aca validamos que todos los lugares que van a ir las letras
        en el tablero sean validos. En caso de que haya lugares ocupados,
        nos devolvera False
    """
    ok = True
    for i in range(tamanio_pal):
        if (orientacion == 0):
            lugar_aux = lugar[0], lugar[1]+i
        else:
            lugar_aux = lugar[0]+i, lugar[1]
        # print('verificando lugar...', lugar_aux) #test
        # print('lugares no disponibles ',lugares_no_disponibles) #test
        if lugar_aux in lugares_no_disponibles:
            ok = False
    # print('Se puede poner?.....', ok)  # test
    return ok


def colocar_en_tablero(window, palabra_a_colocar, letras_usadas_en_tablero,
                       lugar, letras_atril_rival, lugares_no_disponibles, x,
                       y, orientacion, tamanio_pal, l2_guar):
    """
        En este metodo colocamos las letras de las palabras en el tablero,
        recorremos la palabra y por cada letra, la agregamos al tablero,
        la removemos del atril, y guardamos los lugares no disponibles a
        la lista de lugares ocupados en el tablero
    """
    for i, l in zip(range(tamanio_pal), palabra_a_colocar):
        if (orientacion == 0):
            lugar_aux = lugar[0], lugar[1]+i
        else:
            lugar_aux = lugar[0]+i, lugar[1]
        # print(lugar, ': lugar=lugar_aux :', lugar_aux) # test
        letras_usadas_en_tablero.append(l)
        # print('poniendo en el lugar...', lugar_aux)
        window[lugar_aux].update(l.upper(), button_color=('black', 'oldlace'))
        letras_atril_rival.remove(l.upper())
        lugares_no_disponibles.append(lugar_aux)
        l2_guar.extend(l.upper())


def chequeo_y_colocacion(tamanio_pal, x, y, lugar, lugar_aux,
                         lugares_no_disponibles, orientacion, window,
                         palabra_a_colocar, letras_usadas_en_tablero,
                         letras_atril_rival, l2_guar):
    """
        Metodo general en el cual se chequean las palabras y se colocan en el
        tablero
    """
    print('lugar que va a chequear...', lugar)
    print('cordenadas check...', x, ' ', y, ' orientacion ', orientacion)
    ok = todas_los_posiciones_validas(
        tamanio_pal, lugar, lugar_aux, lugares_no_disponibles, orientacion)
    if (ok):
        colocar_en_tablero(
            window, palabra_a_colocar, letras_usadas_en_tablero, lugar,
            letras_atril_rival, lugares_no_disponibles, x, y, orientacion,
            tamanio_pal, l2_guar)

    return ok


def cambiar_orientacion(orientacion):
    if orientacion == 1:
        orientacion = 0
    elif orientacion == 0:
        orientacion = 1
    return orientacion


def seteando_orientacion(tamanio_pal, cord1, cord2, lugar, lugar_aux,
                         lugares_no_disponibles, orientacion, window,
                         palabra_a_colocar, letras_usadas_en_tablero,
                         letras_atril_rival, l2_guar):
    """
       En este metodo nos llegaran el lugar, la palabra a colocar y la
       orientacion, y  se analizan los casos posibles para colocarla en
       el tablero.
       Primero verifica que entre en la orientacion deseada, luego en caso de
       no poder se intentara poner desde el mismo lugar que se deseaba
       pero en la orientacion contraria, y en caso de no poder nos avisara
       que no se puedo colocar
    """
    print('palabra_a_colocar.....', palabra_a_colocar)
    print('x...', cord1, ', y...', cord2)
    print('orientacion...', orientacion)
    print('lugar que llega...', lugar)
    ok = False
    if orientacion == 0:
        print(tamanio_pal-1, '+', cord2, '< 15')
        # si es horizontal chequeamos que y sea valida
        if (((tamanio_pal-1)+cord2) < 15):
            print('cordenadas horziontal...', cord1, ' ',
                  cord2, ' orientacion ', orientacion)
            ok = chequeo_y_colocacion(tamanio_pal, cord1, cord2, lugar,
                                      lugar_aux, lugares_no_disponibles,
                                      orientacion, window,
                                      palabra_a_colocar,
                                      letras_usadas_en_tablero,
                                      letras_atril_rival, l2_guar)
        else:
            print('cordenadas horziontal NO ENTRAN, VEAMOS SI ENTRAN DE FORMA',
                  'VERTICAL...', tamanio_pal-1, '+', cord2, '< 15')
            orientacion = 1
            if (((tamanio_pal-1)+cord1) < 15):
                ok = chequeo_y_colocacion(tamanio_pal, cord2, cord1, lugar,
                                          lugar_aux, lugares_no_disponibles,
                                          orientacion, window,
                                          palabra_a_colocar,
                                          letras_usadas_en_tablero,
                                          letras_atril_rival, l2_guar)

    elif orientacion == 1:
        print(tamanio_pal-1, '+', cord1, '< 15')
        # si es vertical chequeamos que x sea valida
        if (((tamanio_pal-1)+cord1) < 15):
            print('cordenadas vertical...', cord1, ' ',
                  cord2, ' orientacion ', orientacion)
            ok = chequeo_y_colocacion(tamanio_pal, cord1, cord2, lugar,
                                      lugar_aux, lugares_no_disponibles,
                                      orientacion, window,
                                      palabra_a_colocar,
                                      letras_usadas_en_tablero,
                                      letras_atril_rival, l2_guar)
        else:
            print('cordenadas vertical NO ENTRAN, VEAMOS SI ENTRAN DE FORMA',
                  'HORIZONTAL...', tamanio_pal-1, '+', cord2, '< 15')
            orientacion = 0
            print(tamanio_pal-1, '+', cord2, '< 15')
            if (((tamanio_pal-1)+cord2) < 15):
                ok = chequeo_y_colocacion(tamanio_pal, cord2, cord1, lugar,
                                          lugar_aux, lugares_no_disponibles,
                                          orientacion, window,
                                          palabra_a_colocar,
                                          letras_usadas_en_tablero,
                                          letras_atril_rival, l2_guar)
    else:
        sg.popup('No entra la palabra')

    if (not ok):
        sg.popup('No entra la palabra')
    return ok


def buscar_lugar_disponible(window, letras_atril_rival, lugar,
                            lugares_no_disponibles, cant,
                            bolsa_total, letras_usadas_en_tablero,
                            dificultad, l2_guar):
    """
        Para el turno de la maquina Buscamos un lugar en el tablero de forma
        aleatoria en el cual colocaremos la palabra, en caso de no tener
        palabras validas, pasa el turno
    """
    # pasa la lista a minusculas xq las permutaciones no las reconocen las
    # letras en mayuscula
    letras_atril_rival_aux = [x.lower() for x in letras_atril_rival]
    # obtenemos una lista con las posibles palabras
    palabras_posibles = buscar_palabras_rival(
        letras_atril_rival_aux)
    # intentamos obtener alguna palabra de la lista, en caso que la lista no
    # tenga palabras validas
    # se pasa el turno
    puntos_npc = 0
    try:
        # obtenemos alguna de las palabras posibles de la lista al azar si es
        # posible
        palabra_a_colocar = random.choice(palabras_posibles)
        # Ya tenemos la palabra, ahora buscamos lugar disponible
        ok = False
        while (not ok) & (cant < 3):
            x = random.choice(range(0, 15))
            y = random.choice(range(0, 15))
            lugar = (x, y)
            cant += 1
            # Primero vemos si el lugar seleccionado esta disponible
            if lugar not in lugares_no_disponibles:
                # orientacion si la variable es 0 , va a intentar primero
                # poner la palabra horizontalnen caso contrario, si es 1 va
                # intentar ponerla en vertical
                orientacion = random.choice(range(0, 2))
                tamanio_pal = len(palabra_a_colocar)
                lugar_aux = lugar
                # Segundo vemos si la palabra no se va de los limites
                ok = seteando_orientacion(tamanio_pal, x, y, lugar, lugar_aux,
                                          lugares_no_disponibles, orientacion,
                                          window, palabra_a_colocar,
                                          letras_usadas_en_tablero,
                                          letras_atril_rival, l2_guar)
        ##########################################################################################################################################
        # necesito una lista de coords que son los ultimos de lugares_no_disponibles
        lista_coords = []
        for i in range(1, tamanio_pal+1):
            element = lugares_no_disponibles[-i]
            lista_coords.append(element)
        lista_coords.reverse()
        # ahora tengo "letras_usadas_en_tablero" y "lista_coords" si esta bien hecho puedo recorrer las dos listas y usar las funciones de
        # que ya tenemos y no nececitams hacer otro
        for i in range(tamanio_pal):
            aux = puntos_de_letra(letras_usadas_en_tablero[i], dificultad,
                                  lista_coords[i])
            # print('valor de letra...',aux, 'letra',letras_usadas_en_tablero[i])
            puntos_npc = puntos_npc + aux
        # print('valor de total...',puntos_npc)
        for i in range(tamanio_pal):
            puntos_npc2 = puntos_de_palabra(
                dificultad, lista_coords[i], puntos_npc)
        # print('valor de total con modificador...',puntos_npc2)
        ##########################################################################################################################################
        for i in range(len(letras_usadas_en_tablero)):
            letra = crear_atril(bolsa_total)
            letras_atril_rival.append(letra)
        letras_usadas_en_tablero.clear()
        return puntos_npc
    except (IndexError):
        sg.Popup('La maquina no tiene palabras validas para',
                 'colocar pasa el turno')
        return 0


def turno_maquina(window, letras_atril_rival, lugar, lugares_no_disponibles,
                  turno, bolsa_total, letras_usadas_en_tablero, dificultad, l2_guar):
    """
        Comienza el turno de la maquina:
        - La maquina tendra 3 intentos para buscar lugar disponible,
          en caso de no encontrarlo debera pasar el turno
        - en la funcion buscar_lugar_disponible se desarrolla la parte
          de buscar una palabra valida, un lugar disponible, y colocar
          la palabra en el tablero
    """
    sg.Popup('Turno de la maquina')
    cant = 0  # intentos para buscar palabras en cada turno inicializa en 0
    puntos = buscar_lugar_disponible(window, letras_atril_rival,
                                     lugar, lugares_no_disponibles, cant,
                                     bolsa_total, letras_usadas_en_tablero,
                                     dificultad, l2_guar)

    return puntos, 'player_1'


#############################################################
# Aca escribo para los puntos de la IA
#
# Con:
# reutilizar las funciones "puntos_de_letra" y "puntos_de_palabra"
# agrego una var aux: "puntos_npc"
#
# Como:
#
# 'puntos_npc = puntos_de_letra(letra, dificultad, coord)'
#
# 'return puntos_de_palabra(dificultad, lugares_no_disponibles, puntos_npc)'
#
# ver lineas 647
# ============================= FIN IA =============================
