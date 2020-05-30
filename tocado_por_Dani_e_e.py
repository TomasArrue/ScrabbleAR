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
            if (i==0 or i==int(max_Cant_Filas/2) or i==(max_Cant_Filas-1))and(j==0 or j==int(max_Cant_Filas/2) or j==(max_Cant_Filas-1)):#PINTA EN DIAGONAL
                window[i,j].update(button_color=('goldenrod','goldenrod')) 
            if (i==int(max_Cant_Filas/2))&(j==int(max_Cant_Filas/2)):#PINTA EL CENTRO
                window[i,j].update(button_color=('grey','grey'))
            if ((i==1 or i==int(max_Cant_Filas-2))and(j==(int(max_Cant_Filas/2)-2) or j==(int(max_Cant_Filas/2)+2)))or((i==(int(max_Cant_Filas/2)-2) or i==(int(max_Cant_Filas/2)+2))and(j==1 or j==int(max_Cant_Filas-2)))or ((i==(int(max_Cant_Filas/2)-1) or i==(int(max_Cant_Filas/2)+1)) and (j==(int(max_Cant_Filas/2)-1) or j==(int(max_Cant_Filas/2)+1))):
                window[i,j].update(button_color=('skyblue','skyblue'))
            if ((i==0 or i==(max_Cant_Filas-1) or i==int(max_Cant_Filas/2))and(j==3 or j==int(max_Cant_Filas-4)))or((i==3 or i==int(max_Cant_Filas-4))and(j==0 or j==(max_Cant_Filas-1) or j==int(max_Cant_Filas/2)))or((i==(int(max_Cant_Filas/2)-1) or i==(int(max_Cant_Filas/2)+1)) and (j==2 or j==int(max_Cant_Filas-3)))or((i==2 or i==int(max_Cant_Filas-3)) and (j==(int(max_Cant_Filas/2)-1) or j==(int(max_Cant_Filas/2)+1))):
                window[i,j].update(button_color=('mediumseagreen','mediumseagreen'))  
            if (i in range (1,(int(max_Cant_Filas/2)-1)))or(i in range((int(max_Cant_Filas/2)+2),(max_Cant_Filas-1))):
                if (i==j):
                    window[i,j].update(button_color=('indianred','indianred')) 
                    window[i,(max_Cant_Filas-1)-i].update(button_color=('indianred','indianred')) 


                




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
layout.append([sg.Button('borrar',button_color=color_De_Boton,size=tamanio_Boton_De_Control),sg.Button('SALIR',button_color=color_De_Boton,size=tamanio_Boton_De_Control),sg.Button("PEDIR FICHAS",button_color=color_De_Boton,size=tamanio_Boton_De_Control),sg.Button("pintar",button_color=color_De_Boton,size=tamanio_Boton_De_Control)])

window = sg.Window('SCRABBLE', layout, default_button_element_size=(2,2), auto_size_buttons=False)

#event, values = window.read()

#lleva las letras que ya use
usados = []

#lleva la cuenta de los lugares que ya escribi
disponibles = []

palabraCargada=[]#para cargar la palabra que vamos cargando y verificar si es horizontal o vertical


#para despintar la casilla anterior cuando toco una nueva
ant = ()
lugar = ()

layout2 = layout
while True:
    event, values = window.read()
    
    if event in (None, 'SALIR'):
        break
    else:
         if type(event) is tuple:
             lugar = event
             #pinto el lugar que estoy seleccionando,hago esa pregunta para que no trate de marcar un casillero que ya tiene una letra
             if lugar not in disponibles:
                 window[lugar].update(button_color=('white','skyblue'))
             #digo que si anterior tiene algo que despinte lo anterior
             if (ant) and (ant not in disponibles):
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
                     
                     print(a)
                     palabraCargada.append(letra)
                     if len(palabraCargada)==1: #vemos si es la primera letra, seteamos la orientacion de la palabra
                        vertical=False
                        horizontal=False
                        window[lugar].update(letra, button_color=('white','green'))#pinto de verde
                        box_X_vertical=box_X_horizontal=lugar[1]#estas variables sirven para guardar la cord X horizontal y vertical anterior
                        box_Y_vertical=box_Y_horizontal=lugar[0]#estas variables sirven para guardar la cord Y horizontal y vertical anterior
                        a.remove(letra) #saco la letra de la bolsa
                        #print(a) #PARA TESTEO
                        window[letra].update(visible = False) #saco el boton de esa letra
                        usados.append(letra) #lo agrega a mi lista de usados
                        disponibles.append(lugar)#cargo el lugar que ya use
                     elif len(palabraCargada)==2: #vemos si es la primera letra, seteamos la orientacion de la palabra    
                         if box_X_horizontal+1==lugar[1] and box_Y_horizontal==lugar[0]:
                            print('es horizontal')  
                            horizontal=True 
                            window[lugar].update(letra, button_color=('white','green'))#pinto de verde
                            box_X_horizontal=lugar[1]
                            box_Y_horizontal=lugar[0]
                            a.remove(letra)#saco la letra de la bolsa
                            #print(a) #PARA TESTEO
                            window[letra].update(visible = False)#saco el boton de esa letra
                            usados.append(letra)#lo agrega a mi lista de usados
                            disponibles.append(lugar) #cargo el lugar que ya use
                         else:
                            if box_X_vertical==lugar[1] and box_Y_vertical+1==lugar[0]:
                                print('es vertical')  
                                vertical=True 
                                window[lugar].update(letra, button_color=('white','green'))#pinto de verde
                                box_X_vertical=lugar[1]
                                box_Y_vertical=lugar[0]
                                a.remove(letra)#saco la letra de la bolsa
                                
                                window[letra].update(visible = False)#saco el boton de esa letra
                                usados.append(letra)  #lo agrega a mi lista de usados
                                disponibles.append(lugar)  #cargo el lugar que ya use
                     elif vertical:
                        #print('es verti')  #PARA TESTEO
                        #print( box_Y_vertical+1 ,' y ',lugar[0])#PARA TESTEO
                        if box_X_vertical==lugar[1] and box_Y_vertical+1==lugar[0]:
                            #print( box_Y_vertical+1 ,' y ',lugar[0])#PARA TESTEO
                            #print(letra)#PARA TESTEO
                            window[lugar].update(letra, button_color=('white','green'))#pinto de verde
                            box_X_vertical=lugar[1]
                            box_Y_vertical=lugar[0]
                            a.remove(letra) #saco la letra de la bolsa
                            #print(a) #PARA TESTEO
                            window[letra].update(visible = False) #saco el boton de esa letra
                            usados.append(letra)  #lo agrega a mi lista de usados
                            disponibles.append(lugar)  #cargo el lugar que ya use
                        else:
                            sg.Popup('Lugar Invalido')     
                     elif horizontal:
                            #print('es hori') #PARA TESTEO
                            #print( 'A',box_X_horizontal+1 ,' y ',lugar[1])#PARA TESTEO
                            if box_X_horizontal+1==lugar[1] and box_Y_horizontal==lugar[0]:
                                #print( 'B',box_X_horizontal+1 ,' y ',lugar[1])#PARA TESTEO
                                #print(letra)#PARA TESTEO
                                window[lugar].update(letra, button_color=('white','green'))#pinto de verde
                                box_X_horizontal=lugar[1]
                                box_Y_horizontal=lugar[0]
                                a.remove(letra)#saco la letra de la bolsa
                                #print(a)#PARA TESTEO
                                window[letra].update(visible = False)#saco el boton de esa letra
                                usados.append(letra)#lo agrega a mi lista de usados
                                disponibles.append(lugar) #cargo el lugar que ya use
                            else:
                                sg.Popup('Lugar Invalido')     
                     else:
                         sg.Popup('Lugar Invalido')   
                                
                                
            
         if event == "PEDIR FICHAS":
             a = letrasRandom()
             #ZIP lo que hace es crear una lista de tuplas con las listas que le pasas
             mezcla = zip(usados,a)
             print(mezcla)
             for elem in mezcla:
                 #busco la letra que use,en en ese lugar hago visible el boton y actualizo su texto
                 window[elem[0]].update(elem[1],visible=True)
         elif event == "borrar" : #queria agregar la funcion de borrar pero anda medio mal
                     # event, values = window.read()
                     #window[a[0]].update('sh', button_color=('white','blue'))
                     #asignarValores(window)
                     window[lugar].update("",button_color=('grey','white'))
                     a.append(letra)
                     usados.remove(letra)
                     disponibles.remove(lugar)
                     window[letra].update(visible=True)
         elif event == "pintar":
             asignarValores(window)
window.close() 
