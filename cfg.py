import json
with open('tab.json','w') as t:
    tab = {}
    tab['tab_facil'] = {"indianred":[(7,0),(7,4),(7,10),(7,14),(0,7),(14,7)],"goldenrod":[(7,1),(7,2),(7,3),(7,11),(7,12),(7,13)],"mediumseagreen":[(1,7),(2,7),(3,7),(11,7),(12,7),(13,7)],"skyblue":[(5,6),(7,5),(9,6),(9,8),(5,8),(7,9)]}
    tab['tab_medio'] = {"indianred":[],"goldenrod":[],"mediumseagreen":[],"skyblue":[]}
    tab['tab_dificil'] = {"indianred":[],"goldenrod":[],"mediumseagreen":[],"skyblue":[]}
    json.dump(tab,t,indent=3)


with open('tab.json','r') as t:
    dic = json.load(t)

facil = dic['tab_facil']

print(facil)

#agarro cada color
for colores in facil.keys():
    #me quedo con su lista de coordenaas
    coord = facil[colores]
    #ahora voy a recorrer la lista pintando del color de clave
    for c in coord:
        x,y = c
        print('coord X: ',x,'Coord Y :',y)
        print(colores)


'''PROBATE ESTA LUCASSSSS XDDDDDD
def asignarValores(window,dificultad):
    with open('tab.json','r') as t:
        dic = json.load(t)
    
    tablero_config = dic[dificultad]

    for colores in tablero_config.keys():
        lista_de_cord = tablero_config[colores]
        for par_de_cord in lista_de_cord:
            x,y = par_de_cord 
            window[x,y].update(button_color=(colores,colores))'''
            

    