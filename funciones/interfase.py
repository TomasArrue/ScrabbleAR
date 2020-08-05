import PySimpleGUI as sg

tamanio_Boton_De_Fichas = 2, 2  # tamanio de botones que seran las fichas
tamanio_Boton_De_Control = 15, 1  # tamanio de botones de comenzar y salir
dificultad = ['Facil', 'Medio', 'Dificil']  # combobox
max_Cant_Filas = max_Cant_Columnas = 15  # tamanio de las matrices


def ventan_principal():
    """
        genera el layout con la ventana de inicio del juego
    """
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
    return opciones_de_inicio


def ventana_opciones_de_juego():
    """
        se genera el layout con los botones que se podran usar durante la
        partida
    """
    opciones_de_juego = [
        [sg.Button('Borrar', size=tamanio_Boton_De_Control),
         sg.Button("Evaluar", size=tamanio_Boton_De_Control),
         sg.Button("Repartir De Nuevo", size=tamanio_Boton_De_Control),
         sg.Button("Terminar partida", size=tamanio_Boton_De_Control,
         disabled=True)
         ]
    ]
    return opciones_de_juego


def fichas_propias():
    """
        Genera el layout con las 7 fichas nuestras
    """
    fichas = [[sg.Text("Tus Fichas: ", font=("Chalkboard", 15))],
              [sg.Button('', button_color=('black', 'oldlace'),
                         size=(tamanio_Boton_De_Fichas),
                         key=("Boton_"+str(i+1)), pad=(5, 5)) for i in range(7)
               ]
              ]
    return fichas


def fichas_cpu():
    """
        Genera el layout con las 7 fichas del rival
    """
    fichas_rival = [[sg.Text("Fichas CPU: ", font=("Chalkboard", 15))],
                    [sg.Button('??', size=(
                        tamanio_Boton_De_Fichas), key=("Boton_2_"+str(i+1)),
                        pad=(5, 5)) for i in range(7)]
                    ]
    return fichas_rival


def indice_modificadores():
    """
        Genera el layout con los indicadores de puntos de cada modificador
    """
    botones_indieces = [
        [sg.Button(size=(1, 1), button_color=(
            'black', 'indianred')), sg.Text('Letra +5')],
        [sg.Button(size=(1, 1), button_color=('black', 'skyblue')),
         sg.Text('Palabra /2')],
        [sg.Button(size=(1, 1), button_color=(
            'black', 'goldenrod')), sg.Text('Letra *2')],
        [sg.Button(size=(1, 1), button_color=(
            'black', 'mediumseagreen')), sg.Text('Palabra -(0,10)')],
    ]
    return botones_indieces


def tablero():
    """
       genera el layout del tablero, con calumnas x filas de botones
    """
    tablero = [
        [sg.Button('', button_color=('grey', 'azure'), size=(1, 1), key=(i, j),
                   pad=(0, 0)) for j in range(max_Cant_Columnas)]
        for i in range(max_Cant_Filas)
    ]
    return tablero


def marcadore_puntaje_tiempo():
    """
        genera el layout de los indicadores de puntajes y tiempo
    """
    puntaje_y_tiempo = [
        [sg.Text('DIFICULTAD',key='que_dificultad')],
        [sg.Text(' ------ TU PUNTAJE ES:', key='tu_puntaje_propio',
                 size=(20, 1), font=("Chalkboard", 10))],
        [sg.Text('0', key='puntaje_propio', font=("Chalkboard", 10))],
        [sg.Text('PUNTAJE DE JUGADA:', font=("Chalkboard", 10))],
        [sg.Text('0', key='puntaje_de_jugada', font=("Chalkboard", 10))],
        [sg.Text('PUNTAJE PC:', font=("Chalkboard", 10))],
        [sg.Text('0', key='puntaje_PC', font=("Chalkboard", 10))],
        [sg.Text('Tiempo', font=('Chalkboard', 15))],
        [sg.Text('00:00', font=('Chalkboard', 15), key='-OUTPUT-')],
        [sg.T(' ' * 5)]
    ]
    return puntaje_y_tiempo

def opciones_pista():
    pistas = [
        [sg.Text('Pista:')],           
        [sg.Button(size=(1,1),key='boton_pista', 
                   image_filename='./image/pista.png',
                   border_width=1)]]
    return pistas               

def layout_general(fichas_rival, opciones_de_inicio, tablero, puntaje_y_tiempo,
                   botones_indieces, fichas, opciones_de_juego, pista):
    """
        genera el layout principal con los demas generados previamente
    """
    layout = [
        # [sg.Text("Scrabble", size=(8, 1), justification='left',
        #        font=("Chalkboard", 25), relief=sg.RELIEF_RIDGE)],
        [sg.Image('./image/logo.png', key='logo', pad=((70, 60), (0, 0)))],
        [sg.Column(fichas_rival, key='atrilFichasRival',
                   justification='center', visible=False)],
        [sg.Column(opciones_de_inicio, key='opcionesComienzo',
                   justification='left'), sg.Column(tablero),
         sg.Column(puntaje_y_tiempo, key='puntaje', visible=False),
         sg.Frame('Valores de celdas', botones_indieces, key='indice',
                  visible=False)],
        [sg.Column(fichas, key='atrilFichas', justification='center',
                   visible=False)],
        [sg.Column(opciones_de_juego, key='opcionesJuego',
                   justification='center', visible=False)],
        [sg.Column(pista, key='pista',visible=False )]                      
    ]
    return layout


def tablero_default(window):
    """
       vuelve el tablero a su estado inicial para poder pintarse de 0
    """
    [[window[i, j].update(button_color=('black', 'azure')) for j in range(
        max_Cant_Columnas)] for i in range(max_Cant_Filas)]
