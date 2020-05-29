import PySimpleGUI as sg
from random import randint
from string import ascii_uppercase as up
from random import choice
letrasRandom = lambda : [choice(up) for i in range(7)] #Genero 7 letras , serian las que van a la ficha
a=letrasRandom() 

#Prueba de pintado de tablero
def asignarValores(window):
    for i in range(max_Cant_Filas):
        for j in range(max_Cant_Columnas):
            if (i+j==14)|(i==j):#PINTA EN DIAGONAL
                window[i,j].update(button_color=('grey','red')) 
            if (i==7)&(j==7):#PINTA EL CENTRO
                window[i,j].update(button_color=('grey','blue'))    

                




color_De_Boton=('Black','white')
tamanio_Boton_De_Fichas = 2,2 #tamanio de botones que seran las fichas
tamanio_Boton_De_Control = 9,1 #tamanio de botones de comenzar y salir
max_Cant_Filas = max_Cant_Columnas = 15 #tamanio de las matrices
botones_De_Fichas = lambda name : sg.Button(name,button_color=color_De_Boton,size=tamanio_Boton_De_Fichas)

# cambie la key a i + j, solo para que no sea una tupla
layout =  [[sg.Button('',button_color=('grey','white'),size=(2, 2), key=(i,j), pad=(0,0)) for j in range(max_Cant_Columnas)] for i in range(max_Cant_Filas)#botones matriz
          ]
layout.append([sg.Text("Tus Fichas: ")])          
layout.append([botones_De_Fichas(i) for i in a])
layout.append([sg.Button('COMENZAR',button_color=color_De_Boton,size=tamanio_Boton_De_Control),sg.Button('SALIR',button_color=color_De_Boton,size=tamanio_Boton_De_Control),sg.Button("PEDIR FICHAS")])

window = sg.Window('SCRABBLE', layout, default_button_element_size=(2,2), auto_size_buttons=False)

#event, values = window.read()

#lleva las letras que ya use
usados = []

#lleva la cuenta de los lugares que ya escribi
disponibles = []

#para despintar la casilla anterior cuando toco una nueva
ant = ()

while True:
    event, values = window.read()
    
    if event in (None, 'SALIR'):
        break
    else:
         if type(event) is tuple:
             lugar = event

             #pinto el lugar que estoy seleccionando
             window[lugar].update(button_color=('white','skyblue'))

             #digo que si anterior tiene algo que despinte lo anterior
             if (ant):
                 window[ant].update(button_color=('grey','white'))
             ant = lugar
         #print(type(event))
         #print(event) #aca puedes ver que objeto esta recibiendo event, antes recibia una tupla
         #si el evento seria una letra y lugar tiene algo es xq marque algo del tabler
         if event in a and lugar:
                 #asigno la letra del evento
                 letra = event
                 #si el lugar no lo use
                 if lugar not in disponibles:
                     #pinto de verde
                     window[lugar].update(letra, button_color=('white','green'))
                     print(a)
                     #saco la letra de la bolsa
                     a.remove(letra)
                     print(a)
                     #saco el boton de esa letra
                     window[letra].update(visible = False)
                     #lo agrega a mi lista de usados
                     usados.append(letra)
                     #cargo el lugar que ya use
                     disponibles.append(lugar)
                 else:
                     #puede ser que toque un boton que ya tenia algo entonces lo dejo como esta
                     window[lugar].update(button_color=('white','green'))
         if event == "PEDIR FICHAS":
             a = letrasRandom()
             #ZIP lo que hace es crear una lista de tuplas con las listas que le pasas
             mezcla = zip(usados,a)
             print(mezcla)
             for elem in mezcla:
                 #busco la letra que use,en en ese lugar hago visible el boton y actualizo su texto
                 window[elem[0]].update(elem[1],visible=True)
         elif 'COMENZAR' == event :
                     # event, values = window.read()
                     window[a[0]].update('sh', button_color=('white','blue'))
                     asignarValores(window)
         print(event)
         letra2 = event
         print(letra2)
         print(values)
window.close() 

    
    