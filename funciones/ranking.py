import json
import PySimpleGUI as sg

def formet(d):
    """
       formato de texto para mostrar en el ranking
    """
    lista = []
    for k, v in d.items():
        variable = '{} {} --- '.format("Jugador:", v["Nombre"]) + '{} {} --- '.format(
            "Puntaje:", v["Puntos"]) + '{} {}'.format("Fecha:", v["Fecha"])
        lista.append(variable)
    return lista

def ranking():
    """
        generamos una ventana con el ranking en sus diferentes dificulades
         y un ranking general
    """ 
    with open('./texto/ranking_test.json', 'r') as r:
        dicc = json.load(r)

    fac = {}
    med = {}
    dif = {}

    for k, v in dicc.items():
        if v["Dificultad"] == 'facil':
            fac[k] = v
        elif v["Dificultad"] == 'medio':
            med[k] = v
        elif v["Dificultad"] == 'dificil':
            dif[k] = v

    f = sorted(fac.items(), key=lambda k: k[1]["Puntos"], reverse=True)
    m = sorted(med.items(), key=lambda k: k[1]["Puntos"], reverse=True)
    d = sorted(dif.items(), key=lambda k: k[1]["Puntos"], reverse=True)
    total = sorted(dicc.items(), key=lambda k: k[1]["Puntos"], reverse=True)

    rank_facil = formet(dict(f))
    rank_medio = formet(dict(m))
    rank_dif = formet(dict(d))
    rank_total = formet(dict(total))

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
        [sg.Button('Salir')]
    ]
    window2 = sg.Window('TOP TEN').Layout(layout2)
    while True:
        event2, values2 = window2.Read()
        if event2 == 'Salir' or event2 is None:
            break
    window2.Close()