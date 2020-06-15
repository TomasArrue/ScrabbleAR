import json
import PySimpleGUI as sg
with open ('ranking.json','r') as r:
    dicc = json.load(r)

print(dicc.keys())
print(dicc.values())

rank_facil = list(dicc['facil'])
print('valores en facil',rank_facil)

rank_medio = list(dicc['medio'])
print('valores en medio',rank_medio)

rank_dif = list(dicc['dificil'])
print('valores en dificil',rank_dif)

#no me anda la listbox nose xq,la idea es cargar en listbox c/ uno de los valores de los dicc
layout = [[sg.Listbox(values=rank_facil)]]
window = sg.Window(layout)
event,values = window.read()


#Deberia quedar algo asi --->
                #tab1_layout = [[sg.Listbox(rank_facil)]]
               #tab2_layout = [[sg.Listbox(rank_medio)]]
               #tab3_layout = [[sg.Listbox(rank_dif)]]

