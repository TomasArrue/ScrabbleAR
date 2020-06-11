  
import PySimpleGUI as sg
import random
from string import ascii_uppercase as up
from random import choice
from pattern.text.es import lexicon,spelling,verbs

letras=["A","B","C","D","E","F","G","H","I","A",]
letrasRandom = lambda : [choice(up) for i in range(7)] #Genero 7 letras , serian las que van a la ficha
#a=letrasRandom() 
aa=letrasRandom() 
b=letrasRandom() 

#Lista para guardar las coordenadas de de las casillas con color
coordenadas_rojo=[]
coordenadas_dorado=[]
coordenadas_verde=[]
coordenadas_azul=[]
coordenadas_gris=[]

#Prueba de pintado de tablero
def asignarValores(window):

    for i in range(max_Cant_Filas):
        for j in range(max_Cant_Columnas):
            if (i==0 or i==int(max_Cant_Filas/2) or i==(max_Cant_Filas-1))and(j==0 or j==int(max_Cant_Filas/2) or j==(max_Cant_Filas-1)):#PINTA EN DIAGONAL
                window[i,j].update(button_color=('goldenrod','goldenrod')) 
                aux_cord=(i,j)
                coordenadas_dorado.append(aux_cord)
            if (i==int(max_Cant_Filas/2))&(j==int(max_Cant_Filas/2)):#PINTA EL CENTRO
                window[i,j].update(button_color=('grey','grey'))
                aux_cord=(i,j)
                coordenadas_gris.append(aux_cord)
            if ((i==1 or i==int(max_Cant_Filas-2))and(j==(int(max_Cant_Filas/2)-2) or j==(int(max_Cant_Filas/2)+2)))or((i==(int(max_Cant_Filas/2)-2) or i==(int(max_Cant_Filas/2)+2))and(j==1 or j==int(max_Cant_Filas-2)))or ((i==(int(max_Cant_Filas/2)-1) or i==(int(max_Cant_Filas/2)+1)) and (j==(int(max_Cant_Filas/2)-1) or j==(int(max_Cant_Filas/2)+1))):
                window[i,j].update(button_color=('skyblue','skyblue'))
                aux_cord=(i,j)
                coordenadas_azul.append(aux_cord)
            if ((i==0 or i==(max_Cant_Filas-1) or i==int(max_Cant_Filas/2))and(j==3 or j==int(max_Cant_Filas-4)))or((i==3 or i==int(max_Cant_Filas-4))and(j==0 or j==(max_Cant_Filas-1) or j==int(max_Cant_Filas/2)))or((i==(int(max_Cant_Filas/2)-1) or i==(int(max_Cant_Filas/2)+1)) and (j==2 or j==int(max_Cant_Filas-3)))or((i==2 or i==int(max_Cant_Filas-3)) and (j==(int(max_Cant_Filas/2)-1) or j==(int(max_Cant_Filas/2)+1))):
                window[i,j].update(button_color=('mediumseagreen','mediumseagreen')) 
                aux_cord=(i,j)
                coordenadas_verde.append(aux_cord) 
            if (i in range (1,(int(max_Cant_Filas/2)-1)))or(i in range((int(max_Cant_Filas/2)+2),(max_Cant_Filas-1))):
                if (i==j):
                    window[i,j].update(button_color=('indianred','indianred')) 
                    window[i,(max_Cant_Filas-1)-i].update(button_color=('indianred','indianred')) 
                    aux_cord=(i,j)
                    aux_cord2=(i,(max_Cant_Filas-1)-i)
                    coordenadas_rojo.append(aux_cord)
                    coordenadas_rojo.append(aux_cord2)


def volverAPintar(cord,window):
    if cord in coordenadas_rojo: window[cord].update(button_color=('indianred','indianred')) 
    elif cord in coordenadas_dorado: window[cord].update(button_color=('goldenrod','goldenrod')) 
    elif cord in coordenadas_verde: window[cord].update(button_color=('mediumseagreen','mediumseagreen'))
    elif cord in coordenadas_azul: window[cord].update(button_color=('skyblue','skyblue'))
    elif cord in coordenadas_gris: window[cord].update(button_color=('grey','grey')) 
    else: window[cord].update(button_color=('grey','white')) 

                
def verificar_palabra(palabra):
    if palabra in lexicon and spelling or palabra in verbs:
        return True
    else:
        return False   


def obtener_fichas(window,nro_de_boton:str,a:list):
    letra=random.choice(up)
    a.append(letra)
    print(letra)
    window[nro_de_boton].update(letra)    
    window.Refresh()         


def repartir_fichas_de_nuevo(window,cantidad_de_veces_Repartidas:int,a:list): 
    a=[]
    if (cantidad_de_veces_Repartidas < 3):
        cantidad_de_veces_Repartidas=cantidad_de_veces_Repartidas+1
        for i in range(7):#carga de las 7 fichas 
            nro_de_boton='Boton_'+str(i+1)
            obtener_fichas(window,nro_de_boton,a)
    else:
        sg.Popup('Ya hiciste el maximo de cambios de mano')    
    return cantidad_de_veces_Repartidas    


def quitar_fichas(window,usados:list,botones_usados:list,no_disponibles:list):
    #print(len(usados),' ',len(no_disponibles),' ',len(botones_usados))
    if len(usados)>0:# Aca antes de borrar una letra vamos a preguntar si hay letras para borrar, en caso contrario no podras borrar mas letras
        letra_a_borrar=usados.pop(len(usados) - 1)# Saca la ultima letra de la palabra cargada - el pop saca de usados  el elemento de la ultima posicion de la lista de usados
        boton_a_recuperar= botones_usados.pop(len(botones_usados)-1)
        a.append(letra_a_borrar)# vuelve a cargar la letra que sacamos del tablero en el atril de nuestras fichas
        coord_a_liberar=no_disponibles.pop(len(no_disponibles) - 1)# Saca la ultima coordenada de la palabra cargada - el pop saca de no_disponibles el elemento de la ultima posicion de la lista de no_disponibles
        volverAPintar(coord_a_liberar,window) #vuelve a pintar la casilla de su color en estado inicial
        window[coord_a_liberar].update("")
        window[boton_a_recuperar].update(visible=True)
    else:
        sg.Popup('No hay fichas para borrar')   

color_De_Boton=('Black','seagreen')
tamanio_Boton_De_Fichas = 2,2 #tamanio de botones que seran las fichas
tamanio_Boton_De_Control = 15,1 #tamanio de botones de comenzar y salir
max_Cant_Filas = max_Cant_Columnas = 11 #tamanio de las matrices
botones_De_Fichas = lambda name : sg.Button(name,button_color=color_De_Boton,size=tamanio_Boton_De_Fichas)
botones_De_Fichas_rival = lambda name : sg.Button('?',button_color='color_De_Boton',size=tamanio_Boton_De_Fichas)
sg.ChangeLookAndFeel('DarkGrey6')

opciones_de_inicio = [ [sg.Button("Comenzar",size=tamanio_Boton_De_Control)],
                       [sg.Button("Cargar Partida",size=tamanio_Boton_De_Control)], 
                       [sg.Button('Guardar Partida',size=tamanio_Boton_De_Control,visible=False)],      
                       [sg.Button('Salir',size=tamanio_Boton_De_Control,visible=False)] 
                     ]

opciones_de_juego = [ [sg.Button('Borrar',size=tamanio_Boton_De_Control),
                      sg.Button("Pedir Fichas",size=tamanio_Boton_De_Control),
                      sg.Button("Evaluar",size=tamanio_Boton_De_Control),
                      sg.Button("Repartir De Nuevo",size=tamanio_Boton_De_Control)]
                    ]                     

fichas=[ [sg.Text("Tus Fichas: ",font=("Chalkboard", 15))],
         [sg.Button('',button_color=('grey','white'),size=(tamanio_Boton_De_Fichas),key="Boton_1",pad=(5,5)),
          sg.Button('',button_color=('grey','white'),size=(tamanio_Boton_De_Fichas),key="Boton_2",pad=(5,5)),
          sg.Button('',button_color=('grey','white'),size=(tamanio_Boton_De_Fichas),key="Boton_3",pad=(5,5)),
          sg.Button('',button_color=('grey','white'),size=(tamanio_Boton_De_Fichas),key="Boton_4",pad=(5,5)),
          sg.Button('',button_color=('grey','white'),size=(tamanio_Boton_De_Fichas),key="Boton_5",pad=(5,5)),
          sg.Button('',button_color=('grey','white'),size=(tamanio_Boton_De_Fichas),key="Boton_6",pad=(5,5)),
          sg.Button('',button_color=('grey','white'),size=(tamanio_Boton_De_Fichas),key="Boton_7",pad=(5,5))
         ]]  

fichas_rival =[ [sg.Text("Fichas CPU: ",font=("Chalkboard", 15))],
                [botones_De_Fichas_rival(j) for j in b]
              ]  

tablero=[ [sg.Button('',button_color=('grey','white'),size=(2, 2), key=(i,j), pad=(0,0)) for j in range(max_Cant_Columnas)] for i in range(max_Cant_Filas)]#botones matriz

puntaje_y_tiempo=[ [sg.Text('TU PUNTAJE: 0',font=("Chalkboard", 15))],
                   [sg.Text('PUNTAJE PC: 0',font=("Chalkboard", 15))], 
                   [sg.Text('Tiempo',font=('Chalkboard', 15))],
                   [sg.Text('00:00',font=('Chalkboard', 15), key='-OUTPUT-')],#
                   [sg.T(' ' * 5)]
                 ]

layout=[
       [sg.Text("ScrabbleRoll", size=(10, 1), justification='left', font=("Chalkboard", 25), relief=sg.RELIEF_RIDGE)],
       [sg.Column(fichas_rival,key='atrilFichasRival',justification='center',visible=False)],
       [sg.Column(opciones_de_inicio,key='opcionesComienzo',justification='left'), sg.Column(tablero),sg.Column(puntaje_y_tiempo,key='puntaje',visible=False)],
       #[sg.Column(fichas,key='atrilFichas',justification='center',visible=False)],
       [sg.Column(fichas,key='atrilFichas',justification='center',visible=False)],
       [sg.Column(opciones_de_juego,key='opcionesJuego',justification='center',visible=False)],   
       ]

window = sg.Window('SCRABBLE', layout, default_button_element_size=(2,2), auto_size_buttons=False)

a=[]#letras que voy usando
usados = []#lleva las letras que ya use
botones_usados=[]#nombre de los botones que voy usando
no_disponibles = []#lleva la cuenta de los lugares que ya escribi
ant = ()#para despintar la casilla anterior cuando toco una nueva
lugar = ()
layout2 = layout
cantidad_de_veces_Repartidas=0#cantidad de veces de pedidos para hacer el cambio de fichas totales
timer_running, counter = False, 0 #seteos para el timer, 

while True:
    event, values = window.read(timeout=10)
    #event, values = window.read()
    if event in (None, 'Salir'):
        break
    else:
         if type(event) is tuple:
             lugar = event
             if lugar not in no_disponibles: #pinto el lugar que estoy seleccionando,hago esa pregunta para que no trate de marcar un casillero que ya tiene una letra
                 window[lugar].update(button_color=('white','skyblue'))
             if (ant) and (ant not in no_disponibles): #digo que si anterior tiene algo que despinte lo anterior
                 volverAPintar(lugar,window)
             ant = lugar,
         
         if event in  ("Boton_1","Boton_2","Boton_3","Boton_4","Boton_5","Boton_6","Boton_7") and lugar:#si el evento seria una letra y lugar tiene algo es xq marque algo del tabler
                 letra = window[event].GetText()  #asigno la letra del evento
                 if lugar not in no_disponibles: #si el lugar no lo use
                     #usados.append(letra) #lo agrega a mi lista de usados
                     print(letra)
                     if len(usados)==0: #vemos si es la primera letra, seteamos la orientacion de la palabra
                        vertical=False
                        horizontal=False
                        usados.append(letra) #lo agrega a mi lista de usados
                        botones_usados.append(event)
                        window[lugar].update(letra, button_color=('white','green'))#pinto de verde
                        box_X_vertical=box_X_horizontal=lugar[1]#estas variables sirven para guardar la cord X horizontal y vertical anterior
                        box_Y_vertical=box_Y_horizontal=lugar[0]#estas variables sirven para guardar la cord Y horizontal y vertical anterior
                        a.remove(letra) #saco la letra de la bolsa
                        #print(a) #PARA TESTEO
                        window[event].update(visible = False) #saco el boton de esa letra
                        no_disponibles.append(lugar)#cargo el lugar que ya use
                     elif len(usados)==1: #vemos si es la primera letra, seteamos la orientacion de la palabra    
                         if box_X_horizontal+1==lugar[1] and box_Y_horizontal==lugar[0]:
                            print('es horizontal')  
                            horizontal=True
                            usados.append(letra) #lo agrega a mi lista de usados
                            botones_usados.append(event)
                            window[lugar].update(letra, button_color=('white','green'))#pinto de verde
                            box_X_horizontal=lugar[1]
                            box_Y_horizontal=lugar[0]
                            a.remove(letra) #saco la letra de la bolsa
                            #print(a) #PARA TESTEO
                            window[event].update(visible = False) #saco el boton de esa letra
                            no_disponibles.append(lugar)  #cargo el lugar que ya use
                         elif box_X_vertical==lugar[1] and box_Y_vertical+1==lugar[0]:
                            print('es vertical')  
                            vertical=True 
                            usados.append(letra) #lo agrega a mi lista de usados
                            botones_usados.append(event)
                            window[lugar].update(letra, button_color=('white','green'))#pinto de verde
                            box_X_vertical=lugar[1]
                            box_Y_vertical=lugar[0]
                            a.remove(letra) #saco la letra de la bolsa
                            #print(a) #PARA TESTEO
                            window[event].update(visible = False) #saco el boton de esa letra
                            no_disponibles.append(lugar)  #cargo el lugar que ya use
                     elif len(usados)>1:      
                         if vertical:
                             #print('es verti')  #PARA TESTEO
                             #print( box_Y_vertical+1 ,' y ',lugar[0])#PARA TESTEO
                             if box_X_vertical==lugar[1] and box_Y_vertical+1==lugar[0]:
                                 #print( box_Y_vertical+1 ,' y ',lugar[0])#PARA TESTEO
                                 #print(letra)#PARA TESTEO
                                 usados.append(letra) #lo agrega a mi lista de usados
                                 botones_usados.append(event)
                                 window[lugar].update(letra, button_color=('white','green'))#pinto de verde
                                 box_X_vertical=lugar[1]
                                 box_Y_vertical=lugar[0]
                                 a.remove(letra) #saco la letra de la bolsa
                                 #print(a) #PARA TESTEO
                                 window[event].update(visible = False) #saco el boton de esa letra
                                 no_disponibles.append(lugar)  #cargo el lugar que ya use
                             else:
                                 sg.Popup('Lugar Invalido')  
                                  
                         elif horizontal:
                            #print('es hori') #PARA TESTEO
                            #print( 'A',box_X_horizontal+1 ,' y ',lugar[1])#PARA TESTEO
                            if box_X_horizontal+1==lugar[1] and box_Y_horizontal==lugar[0]:
                                #print( 'B',box_X_horizontal+1 ,' y ',lugar[1])#PARA TESTEO
                                #print(letra)#PARA TESTEO
                                usados.append(letra) #lo agrega a mi lista de usados
                                botones_usados.append(event)
                                window[lugar].update(letra, button_color=('white','green'))#pinto de verde
                                box_X_horizontal=lugar[1]
                                box_Y_horizontal=lugar[0]
                                a.remove(letra)#saco la letra de la bolsa
                                #print(a)#PARA TESTEO
                                window[event].update(visible = False)#saco el boton de esa letra
                                no_disponibles.append(lugar) #cargo el lugar que ya use
                            else:
                                sg.Popup('Lugar Invalido')      
                     print('Letras de atril despues de cargar:',a)
                     print(len(usados),' ',len(no_disponibles))              
        
         #print(event)
         if event == "Pedir Fichas":
             a = letrasRandom()
             #ZIP lo que hace es crear una lista de tuplas con las listas que le pasas
             mezcla = zip(usados,a)
             print(mezcla)
             for elem in mezcla:
                 #busco la letra que use,en en ese lugar hago visible el boton y actualizo su texto
                 window[elem[0]].update(elem[1],visible=True)
        
         elif event == "Repartir De Nuevo":
            cantidad_de_veces_Repartidas=repartir_fichas_de_nuevo(window,cantidad_de_veces_Repartidas,a) 
            
         elif event == "Borrar" : #quita elementos del tablero, desde el ultimo al primero  
             quitar_fichas(window,usados,botones_usados,no_disponibles)
       
         elif event == "Comenzar":
             asignarValores(window)
             window['opcionesJuego'].update(visible=True)
             window['Comenzar'].update(visible=False)
             window['Cargar Partida'].update(visible=False)
             window['Guardar Partida'].update(visible=True)
             window['Salir'].update(visible=True)
             window['puntaje'].update(visible=True)
             window['atrilFichasRival'].update(visible=True)
             window['atrilFichas'].update(visible=True)
             for i in range(7):#carga de las 7 fichas al inicio
                nro_de_boton='Boton_'+str(i+1)
                obtener_fichas(window,nro_de_boton,a)
             timer_running = not timer_running


         elif timer_running:
           #  window['-OUTPUT-'].update('{:02d}:{:02d}'.format((counter // 100) // 60, (counter // 100) % 60, counter % 100))
             window['-OUTPUT-'].update('{:02d}:{:02d}'.format((counter // 100) // 60, (counter // 100) % 60))
             counter += 1
             if counter==60000:#600 equivale a 1 minuto, 60000 a 10 minutos
                timer_running = not timer_running
                sg.Popup('termino el tiempo')       


         elif event == "Evaluar": #aca va evaluar,evalua la palabra y resetea las orientaciones
             vertical = False
             horizontal = False
             palabra_final=verificar_palabra("".join(usados))
             print(palabra_final)
             ok = verificar_palabra(palabra_final)
             if not ok:
                 for letra in usados:
                     #while len(usados)>0:# Aca antes de borrar una letra vamos a preguntar si hay letras para borrar, en caso contrario no podras borrar mas letras
                        letra_a_borrar=usados.pop(len(usados) - 1)# Saca la ultima letra de la palabra cargada - el pop saca de usados  el elemento de la ultima posicion de la lista de usados
                        a.append(letra_a_borrar)# vuelve a cargar la letra que sacamos del tablero en el atril de nuestras fichas
                        coord_a_liberar=no_disponibles.pop(len(no_disponibles) - 1)# Saca la ultima coordenada de la palabra cargada - el pop saca de no_disponibles el elemento de la ultima posicion de la lista de no_disponibles
                        volverAPintar(coord_a_liberar,window) #vuelve a pintar la casilla de su color en estado inicial
                        print('Letras de atril cargadas de nuevo: ',a)
                        print(coord_a_liberar)
                        print(letra_a_borrar)
                        window[coord_a_liberar].update("")
                        window[letra_a_borrar].update(visible=True)
                     #window[letra].update(visible=True)
                     #usados.remove(letra)
                     #a.append(letra)
             else: 
                 a = letrasRandom()
                 for r in range(len(a),7): 
                    a.append(choice(up))
                 #ZIP lo que hace es crear una lista de tuplas con las listas que le pasas
                 mezcla = zip(usados,a)
                 print(mezcla)
                 for elem in mezcla:
                     #busco la letra que use,en en ese lugar hago visible el boton y actualizo su texto
                     window[elem[0]].update(elem[1],visible=True)

    window.Refresh()         
    window.Refresh()
    #window.Size=window.Size
#update(atrilNuevo[i])
window.close()

"""cosas pendientes: 
     -hay que terminar de probar el evaluar
     -lo de asignar valores deberia venir en un json ya con los valores y ejecutarlo desde aca,osea crear un json y un modulo que ejecute funciones del tablero 
     -verificar palabra,pedir fichas y borrar  deberia estar dentro de un modulo funciones
     -el atril de letras,por lo que vi es mejor ponerlo dentro de una estructura columna se que esta en gui pero no la pude hacer andar""" 