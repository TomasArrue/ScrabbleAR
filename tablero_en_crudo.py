  
import PySimpleGUI as sg
from random import randint
from string import ascii_uppercase as up
from random import choice
from pattern.text.es import lexicon,spelling,verbs

letrasRandom = lambda : [choice(up) for i in range(7)] #Genero 7 letras , serian las que van a la ficha
a=letrasRandom() 

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



color_De_Boton=('Black','white')
tamanio_Boton_De_Fichas = 1,1 #tamanio de botones que seran las fichas
tamanio_Boton_De_Control = 9,1 #tamanio de botones de comenzar y salir
max_Cant_Filas = max_Cant_Columnas = 11 #tamanio de las matrices
botones_De_Fichas = lambda name : sg.Button(name,button_color=color_De_Boton,size=tamanio_Boton_De_Fichas,key=('fichas'))

# cambie la key a i + j, solo para que no sea una tupla
layout =  [[sg.Button('',button_color=('grey','white'),size=(2, 2), key=(i,j), pad=(0,0)) for j in range(max_Cant_Columnas)] for i in range(max_Cant_Filas)#botones matriz
          ]
layout.append([sg.Text("Tus Fichas: ")])          
layout.append([botones_De_Fichas(i) for i in a])
layout.append([sg.Button('Borrar',button_color=color_De_Boton,size=tamanio_Boton_De_Control),
               sg.Button('Salir',button_color=color_De_Boton,size=tamanio_Boton_De_Control),
               sg.Button("Pedir Fichas",button_color=color_De_Boton,size=tamanio_Boton_De_Control),
               sg.Button("Pintar",button_color=color_De_Boton,size=tamanio_Boton_De_Control),
               sg.Button("Evaluar",button_color=color_De_Boton,size=tamanio_Boton_De_Control),
               sg.Button('Repartir De Nuevo',button_color=color_De_Boton,size=tamanio_Boton_De_Control)])
#w, h = sg.Window.get_screen_size()
window = sg.Window('SCRABBLE', layout, default_button_element_size=(2,2), auto_size_buttons=False)

#event, values = window.read()
#lleva las letras que ya use
usados = []
#lleva la cuenta de los lugares que ya escribi
no_disponibles = []



#para despintar la casilla anterior cuando toco una nueva
ant = ()
lugar = ()

layout2 = layout
while True:
    event, values = window.read()
    
    if event in (None, 'Salir'):
        break
    else:
         if type(event) is tuple:
             lugar = event
             #pinto el lugar que estoy seleccionando,hago esa pregunta para que no trate de marcar un casillero que ya tiene una letra
             if lugar not in no_disponibles:
                 window[lugar].update(button_color=('white','skyblue'))
             #digo que si anterior tiene algo que despinte lo anterior
             if (ant) and (ant not in no_disponibles):
                 volverAPintar(lugar,window)
             ant = lugar
         #print(type(event))
         #print(event) #aca puedes ver que objeto esta recibiendo event, antes recibia una tupla
         #si el evento seria una letra y lugar tiene algo es xq marque algo del tabler
         if event in a and lugar:
                 #asigno la letra del evento
                 letra = event
                 #si el lugar no lo use
                 if lugar not in no_disponibles:
                     #usados.append(letra) #lo agrega a mi lista de usados
                     if len(usados)==0: #vemos si es la primera letra, seteamos la orientacion de la palabra
                        vertical=False
                        horizontal=False
                        usados.append(letra) #lo agrega a mi lista de usados
                        window[lugar].update(letra, button_color=('white','green'))#pinto de verde
                        box_X_vertical=box_X_horizontal=lugar[1]#estas variables sirven para guardar la cord X horizontal y vertical anterior
                        box_Y_vertical=box_Y_horizontal=lugar[0]#estas variables sirven para guardar la cord Y horizontal y vertical anterior
                        a.remove(letra) #saco la letra de la bolsa
                        #print(a) #PARA TESTEO
                        window[letra].update(visible = False) #saco el boton de esa letra
                        no_disponibles.append(lugar)#cargo el lugar que ya use
                     elif len(usados)==1: #vemos si es la primera letra, seteamos la orientacion de la palabra    
                         if box_X_horizontal+1==lugar[1] and box_Y_horizontal==lugar[0]:
                            print('es horizontal')  
                            horizontal=True
                            usados.append(letra) #lo agrega a mi lista de usados
                            window[lugar].update(letra, button_color=('white','green'))#pinto de verde
                            box_X_horizontal=lugar[1]
                            box_Y_horizontal=lugar[0]
                            a.remove(letra) #saco la letra de la bolsa
                            #print(a) #PARA TESTEO
                            window[letra].update(visible = False) #saco el boton de esa letra
                            no_disponibles.append(lugar)  #cargo el lugar que ya use
                         elif box_X_vertical==lugar[1] and box_Y_vertical+1==lugar[0]:
                            print('es vertical')  
                            vertical=True 
                            usados.append(letra) #lo agrega a mi lista de usados
                            window[lugar].update(letra, button_color=('white','green'))#pinto de verde
                            box_X_vertical=lugar[1]
                            box_Y_vertical=lugar[0]
                            a.remove(letra) #saco la letra de la bolsa
                            #print(a) #PARA TESTEO
                            window[letra].update(visible = False) #saco el boton de esa letra
                            no_disponibles.append(lugar)  #cargo el lugar que ya use
                     elif len(usados)>1:      
                         if vertical:
                             #print('es verti')  #PARA TESTEO
                             #print( box_Y_vertical+1 ,' y ',lugar[0])#PARA TESTEO
                             if box_X_vertical==lugar[1] and box_Y_vertical+1==lugar[0]:
                                 #print( box_Y_vertical+1 ,' y ',lugar[0])#PARA TESTEO
                                 #print(letra)#PARA TESTEO
                                 usados.append(letra) #lo agrega a mi lista de usados
                                 window[lugar].update(letra, button_color=('white','green'))#pinto de verde
                                 box_X_vertical=lugar[1]
                                 box_Y_vertical=lugar[0]
                                 a.remove(letra) #saco la letra de la bolsa
                                 #print(a) #PARA TESTEO
                                 window[letra].update(visible = False) #saco el boton de esa letra
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
                                window[lugar].update(letra, button_color=('white','green'))#pinto de verde
                                box_X_horizontal=lugar[1]
                                box_Y_horizontal=lugar[0]
                                a.remove(letra)#saco la letra de la bolsa
                                #print(a)#PARA TESTEO
                                window[letra].update(visible = False)#saco el boton de esa letra
                                no_disponibles.append(lugar) #cargo el lugar que ya use
                            else:
                                sg.Popup('Lugar Invalido')      
                     print('Letras de atril despues de cargar:',a)
                     print(len(usados),' ',len(no_disponibles))              
         if event == "Pedir Fichas":
             a = letrasRandom()
             #ZIP lo que hace es crear una lista de tuplas con las listas que le pasas
             mezcla = zip(usados,a)
             print(mezcla)
             for elem in mezcla:
                 #busco la letra que use,en en ese lugar hago visible el boton y actualizo su texto
                 window[elem[0]].update(elem[1],visible=True)
         elif event == "Borrar" : #queria agregar la funcion de borrar pero anda medio mal
                     
                     #event, values = window.read()
                     #window[a[0]].update('sh', button_color=('white','blue'))
                     #asignarValores(window)
                     print(len(usados),' ',len(no_disponibles))

                     if len(usados)>0:# Aca antes de borrar una letra vamos a preguntar si hay letras para borrar, en caso contrario no podras borrar mas letras
                        letra_a_borrar=usados.pop(len(usados) - 1)# Saca la ultima letra de la palabra cargada - el pop saca de usados  el elemento de la ultima posicion de la lista de usados
                        a.append(letra_a_borrar)# vuelve a cargar la letra que sacamos del tablero en el atril de nuestras fichas
                        coord_a_liberar=no_disponibles.pop(len(no_disponibles) - 1)# Saca la ultima coordenada de la palabra cargada - el pop saca de no_disponibles el elemento de la ultima posicion de la lista de no_disponibles
                        volverAPintar(coord_a_liberar,window) #vuelve a pintar la casilla de su color en estado inicial
                        print('Letras de atril cargadas de nuevo: ',a)
                        print(coord_a_liberar)
                        print(letra_a_borrar)
                        window[coord_a_liberar].update("")
                        window[letra_a_borrar].update(visible=True)
                     else:
                         sg.Popup('No hay fichas para borrar')   
         elif event == "Pintar":
             asignarValores(window)
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
         elif event=='Repartir De Nuevo' :
             atrilNuevo=letrasRandom() 
             print(atrilNuevo)
             #for i in range(len(a)):  
             #   print(window['name'].Key)
             #botones_De_Fichas(i) for i in a
#update(atrilNuevo[i])
window.close()

"""cosas pendientes: 
     -hay que terminar de probar el evaluar
     -lo de asignar valores deberia venir en un json ya con los valores y ejecutarlo desde aca,osea crear un json y un modulo que ejecute funciones del tablero 
     -verificar palabra,pedir fichas y borrar  deberia estar dentro de un modulo funciones
     -el atril de letras,por lo que vi es mejor ponerlo dentro de una estructura columna se que esta en gui pero no la pude hacer andar""" 
