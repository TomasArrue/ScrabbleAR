import PySimpleGUI as sg
import funciones as f

bolsa_letras = f.bolsa_de_letras

bolsa_jugador = []

bolsa_maquina = []

f.crear_bolsas(bolsa_letras,bolsa_jugador,bolsa_maquina)


print(bolsa_jugador)



def pintarTablero(matriz,g):
    #ACA DIBUJAMOS EL TABLERO
    rango=15
    for row in range(rango):
            for col in range(rango):
                #EN ESTA PARTE HACEMOS LAS DIVISIONES DE LAS CELDAS CON UNA LINEA BLANCA
                matriz[row][col]=g.DrawRectangle((col * tam_celda + 5, row * tam_celda + 3), 
                                                (col * tam_celda + tam_celda + 5, row * tam_celda + tam_celda + 3),
                                                line_color='white')
                #ACA PINTAMOS LAS CELDAS COLOR DORADO                                
                if (row==0 or row==7 or row==14)and(col==0 or col==7 or col==14):
                        matriz[row][col]=g.DrawRectangle((col * tam_celda + 5, row * tam_celda + 3),
                                                        (col * tam_celda + tam_celda + 5, row * tam_celda + tam_celda + 3),
                                                        fill_color='goldenrod',line_color='white')
                #ACA PINTAMOS LAS CELDAS COLOR CELESTE                                
                if ((row==1 or row==13)and(col==5 or col==9))or((row==5 or row==9)and(col==1 or col==13))or ((row==6 or row==8) and (col==6 or col==8)):
                        matriz[row][col]=g.DrawRectangle((col * tam_celda + 5, row * tam_celda + 3),
                                                        (col * tam_celda + tam_celda + 5, row * tam_celda + tam_celda + 3),
                                                        fill_color='skyblue',line_color='white')
                #ACA PINTAMOS LAS CELDAS COLOR VERDE                                
                if ((row==0 or row==14 or row==7)and(col==3 or col==11))or((row==3 or row==11)and(col==0 or col==14 or col==7))or((row==6 or row==8) and (col==2 or col==12))or((row==2 or row==12) and (col==6 or col==8)):
                        matriz[row][col]=g.DrawRectangle((col * tam_celda + 5, row * tam_celda + 3),
                                                        (col * tam_celda + tam_celda + 5, row * tam_celda + tam_celda + 3),
                                                        fill_color='mediumseagreen',line_color='white')
                #ACA PINTAMOS LAS CELDAS COLOR ROJO
                if (row in range (1,6))or(row in range(9,14)):
                    if (row==col):  
                        matriz[row][col]=g.DrawRectangle((col * tam_celda + 5, row * tam_celda + 3),
                                                        (col * tam_celda + tam_celda + 5, row * tam_celda + tam_celda + 3),
                                                         fill_color='indianred',line_color='white')                                 
                        matriz[row][((rango-1)-row)]=g.DrawRectangle((((rango-1)-row) * tam_celda + 5, row * tam_celda + 3),
                                                        (((rango-1)-row) * tam_celda + tam_celda + 5, row * tam_celda + tam_celda + 3),
                                                        fill_color='indianred',line_color='white')  


tam_celda =15

button = lambda name : sg.Button(name)

layout = [
         [sg.T(' ' * 5)],
         [sg.Graph((500,500),(0,232),(235,0), key='_GRAPH_', background_color='gainsboro',change_submits=True, drag_submits=False)],
         [button(i) for i in bolsa_jugador],[button(i) for i in bolsa_maquina],
         [sg.Button("Evaluar")]]

window = sg.Window('Ejercicio1', ).Layout(layout).Finalize()
g = window.FindElement('_GRAPH_')

matriz=[]
selected=[]
text_box=[]
for i in range(0,15):
    matriz.append([0]*15)
    selected.append([False]*15)
    text_box.append([""]*15)
#ACA DIBUJAMOS EL TABLERO
pintarTablero(matriz,g)


while True:
    event, values = window.Read()
    print(values)
    if event is None or 'tipo' == 'Exit':
        break