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
layout.append([sg.Button('COMENZAR',button_color=color_De_Boton,size=tamanio_Boton_De_Control),sg.Button('SALIR',button_color=color_De_Boton,size=tamanio_Boton_De_Control)])

window = sg.Window('SCRABBLE', layout, default_button_element_size=(2,2), auto_size_buttons=False)

#event, values = window.read()

while True:
    event, values = window.read()
    
    if event in (None, 'SALIR'):
        break
    else:
                    print(event) #aca puedes ver que objeto esta recibiendo event, antes recibia una tupla
                    if event in a:
                                     keys_entered = event
                                     event, values = window.read()
                                     window[event].update(keys_entered, button_color=('white','green'))

                    elif 'COMENZAR' == event :
                                     # event, values = window.read()
                                     window[a[0]].update('sh', button_color=('white','blue'))
                                     asignarValores(window)
                                    # print(event)
window.close() 

    
    