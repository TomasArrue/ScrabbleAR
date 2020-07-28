import PySimpleGUI as sg
import json
import random



def formet(d):
    lista = []
    for k, v in d.items():
        variable = '{} {} --- '.format("Jugador:", v["Nombre"]) + '{} {} --- '.format(
            "Puntaje:", v["Puntos"]) + '{} {}'.format("Fecha:", v["Fecha"])  
        lista.append(variable)   
    return lista

with open('./texto/ranking_test2.json', 'r') as r:
     dicc = json.load(r)
'''
     fac = dicc['facil']
     med = dicc['medio']
     dif = dicc['dificil']
     

     for (key, value) in sorted(dif.items(), key=lambda x: x[1]["Puntos"],reverse=True):
          print(key, value) 

     f = sorted(fac.items(), key=lambda k: k[1]["Puntos"], reverse=True)
     m = sorted(med.items(), key=lambda k: k[1]["Puntos"], reverse=True)
     d = sorted(dif.items(), key=lambda k: k[1]["Puntos"], reverse=True)
     #total=  sorted(total.items(), key=lambda k: k[1][1]["Puntos"], reverse=True)

     #print(d)
     #print(total)
'''
fac={}
med={}
dif={}
for k, v in dicc.items():
     if v["Dificultad"]=='facil':
          fac[k] = v 
     elif v["Dificultad"]=='medio':
          med[k] = v      
     elif v["Dificultad"]=='dificil':
          dif[k] = v      

#print('Puntajes de facil, ...',fac)
#print('Puntajes de medio, ...',med)
#print('Puntajes de dificil, ...',dif)

f = sorted(fac.items(), key=lambda k: k[1]["Puntos"], reverse=True)
m = sorted(med.items(), key=lambda k: k[1]["Puntos"], reverse=True)
d = sorted(dif.items(), key=lambda k: k[1]["Puntos"], reverse=True)
total= sorted(dicc.items(), key=lambda k: k[1]["Puntos"], reverse=True, )

#print ('Puntajes de facil ordenados, ...',f)
#print ('Puntajes de medio ordenados, ...',m)
#print ('Puntajes de dificil ordenados, ...',d)

#print ('Puntajes de dificil ordenados, ...',total)


rank_facil = formet(dict(f))

rank_total = formet(dict(total))

for k in rank_total:
     print(k)

print('facil')
for k in rank_facil:
     print(k)
##sg.theme('Dark Brown 1')

with open('./texto/ranking_test2.json', 'w') as j:
     id=str(random.choice(range(0,10000)))

     dicc['id_'+id] = {"Dificultad": 'dificult',
                         "Nombre":'nombre',
                         "Puntos": 2222,
                         "Fecha": 0}

     json.dump(dicc, j, indent=4)   
'''
headings = ['NOMBRE', 'PUNTOS', 'FECHA']
header =  [[sg.Text('')] + [sg.Text(h, size=(14,1)) for h in headings]]


input_rows = [[sg.Input(key=(col,row),size=(15,1), pad=(0,0)) for col in range(3)] for row in range(10)]

layout = header + input_rows

window = sg.Window('Table Simulation', layout, font='Courier 12')

print(f)

for  k in f:
     for row in range(10):
          for col in range(3):
               lugar=(col,row)
               window[lugar].Update(k[1]['Puntos'])

event, values = window.read()

     

#print ('cap',col,row)
  
for k, v in f.items():
     window[c]v["Nombre"]
     v["Puntos"]
     v["Fecha"]
     
rank_facil = funciones.formet(dict(f))

'''

