import json
import PySimpleGUI as sg


def config_por_defecto():
    with open('./texto/config_default.json', 'r') as cf:
        c = json.load(cf)
    with open('./texto/config.json', 'w') as cf:
        json.dump(c, cf, indent=4)
    sg.popup('Se restauro la configuracion inicial :D')


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
        [sg.Text("Configuracion", size=(10, 1), justification='left',
                 font=("Chalkboard", 25), relief=sg.RELIEF_RIDGE)],
        [sg.Text(k, size=(3, 1), justification='center')
         for k, v in diccionario_cantidad_de_letras.items()],
        [sg.Text('PARA MODIFICAR LA CANTIDAD DE LETRAS POR LETRA CAMBIE EL VALOR A LA LETRA CORRESPONDIENTE :')],
        [sg.Input(v, size=(3, 1), key=(k+'_cant'))
         for k, v in diccionario_cantidad_de_letras.items()],
        [sg.Text('PARA MODIFICAR EL VALOR DE LAS LETRAS POR LETRA CAMBIE EL VALOR A LA LETRA CORRESPONDIENTE:')],
        [sg.Input(v, size=(3, 1), key=(k+'_valor'))
         for k, v in diccionario_cantidad_de_puntos.items()],
        [sg.Text('')], [sg.Text(
            'PARA MODIFICAR EL TIEMPO INGRESE EL TIEMPO EN MINUTOS (de 5 a 30) QUE QUIERES QUE DURE LA PARTIDA')],
        [sg.Input(size=(9, 1), key=('time'))],
        [sg.Button('CONFIGURACION POR DEFECTO'), sg.Button(
            'GUARDAR CONFIGURACION'), sg.Button('CANCELAR')]
    ]

    window3 = sg.Window('Configuracion').Layout(layout3)

    while True:

        event3, values3 = window3.Read()

        if event3 == 'CANCELAR' or event3 is None:
            break

        if event3 == 'CONFIGURACION POR DEFECTO':
            config_por_defecto()
            break

        if event3 == 'GUARDAR CONFIGURACION':
            # with open('config.json','w') as cf:
            try:
                num_tiempo = int(values3['time'])
                if (num_tiempo > 30):
                    num_tiempo = 30
                if (num_tiempo < 1):
                    num_tiempo = 1
            except (ValueError):
                # seteamos 10 minutos en caso de cargar erronea de tiempo
                num_tiempo = 10
                sg.Popup('El tiempo se cargo de maneara erronea, pero ',
                         'cargamos la partida de 10 minutos')

            for k, v in diccionario_cantidad_de_letras.items():

                try:
                    if int(values3[k+'_cant']) > 0:
                        diccionario_cantidad_de_letras[k] = int(
                            values3[k+'_cant'])
                    else:
                        diccionario_cantidad_de_letras[k] = 1
                except (ValueError):
                    diccionario_cantidad_de_letras[k] = 1
                try:
                    if int(values3[k+'_valor']) > 0:
                        diccionario_cantidad_de_puntos[k] = int(
                            values3[k+'_valor'])
                    else:
                        diccionario_cantidad_de_puntos[k] = 1
                except (ValueError):
                    diccionario_cantidad_de_puntos[k] = 1
            tiempo = {'minutos': num_tiempo}
            with open('./texto/config.json', 'w') as cf:
                c['cantidad_de_letras'] = diccionario_cantidad_de_letras
                c['valor_por_letra'] = diccionario_cantidad_de_puntos
                c['tiempo'] = tiempo
                json.dump(c, cf, indent=4)

            sg.Popup('La duracion de la partida sera de: ',
                     num_tiempo, ' minutos')
            sg.popup('Se configuro la partida')
            break

    window3.close()
