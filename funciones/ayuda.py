import PySimpleGUI as sg


def menu():
    
    primero = '''    Para colocar una letra en el tablero primero debe seleccionar una casilla libre y luego deberá seleccionar la letra a colocar dentro de su atril
              
    Para jugar la palabra escrita en el tablero oprima el boton "Evaluar y se chequeará si la palabra corresponde a la clasificación que se está usando en el juego. Se recuerda que las únicas palabras admitidas en el tablero serán adjetivos, sustantivos y verbos, de acuerdo a las opciones de configuración establecidas previamente. En caso de no corresponder, las fichas serán devueltas al jugador para que vuelva a intentar.  

    En cualquier momento del juego, el jugador puede decidir usar un turno para cambiar todas sus fichas, devolviéndolas a la bolsa de fichas del juego y reemplazándolas por la misma cantidad; al final, siempre debe tener siete (7). El jugador sólo podrá usarla como máximo tres veces durante el juego.

    El juego termina cuando el jugador en turno no puede completar sus siete (7) fichas luego de una jugada, dado que no hay más fichas en la bolsa de fichas del juego; se acabó el tiempo de la partida'''

    botones_indieces = [
        [sg.Button(size=(1, 1), button_color=(
            'black', 'indianred')), sg.Text('Las letra dentro de las casillas de este color suman +5 puntos',size=(60, 2),text_color='red')],
        [sg.Button(size=(1, 1), button_color=(
            'black', 'goldenrod')), sg.Text('Las letra dentro de las casillas de este color suman  x2 puntos',size=(60, 2),text_color='yellow')],
        [sg.Button(size=(1, 1), button_color=(
            'black', 'mediumseagreen')), sg.Text('Si la palabra generada pasa por alguna de las casillas de este color, \n el puntaje de la palabra se resta por algun valor entre 0 y 10',size=(60, 3),text_color='green')],
        [sg.Button(size=(1, 1), button_color=(
            'black', 'skyblue')), sg.Text('Si la palabra generada pasa por alguna de las casillas de este color, \n el puntaje de la palabra se divide por 2 ',size=(60, 3),text_color='skyblue')]    
    ]    
    layout2 = [
        [sg.Text('Algunas reglas basicas para el juego:',font=('Arial',15)), sg.Text('', key='_AYUDA_')],
        [sg.Multiline(primero,size=(60,20))],
        [sg.Text('Algunas celdas tienen propiedades especiales las cuales se identifican con diferenes colores:')],
        [sg.Frame('Valores de celdas', botones_indieces)],
        [sg.Button('Salir')]
    ]
    window2 = sg.Window(' AYUDA ').Layout(layout2)
    while True:
        event2, values2 = window2.Read()
        if event2 == 'Salir' or event2 is None:
            break
    window2.Close()