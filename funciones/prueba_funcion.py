def funcion_1():
    print("el import funcionaaaaa")
    archivo = open("./texto/hola.txt", "r") 
    # el punto inicial en la ruta hace referencia al directorio donde se encuentra 
    # el archivo que llama a ejecutar esta funcion. (en este caso concreto "prueba_tom.py")
    # no busca desde donde esta declarada la funcion sino desde se la invoca.
    print(archivo.read())
    archivo.close()