from funciones.general import *
from tablaHash import TablaHash

ruta = "ArchNombres1.txt"

datos=cargarDatos(ruta)
print(datos)

while True:
    try:
        tamanio=input("Ingrese el tamaño de la tabla: ")
        tamanio=int(tamanio)
    except ValueError:
        print("El valor debe ser un número")
    else:
        if tamanio<len(datos):
            print("El tamaño no puede ser menor que la cantidad de datos")
        else:
            break

tabla=TablaHash(tamanio, 2, 2, ruta)
tabla.setPaso(3)
for i in range(len(datos)):
    num=datos[i][0]
    tabla.ingresarDatos(int(num),i+1)
print("")
print(tabla)
print("")
print(tabla.getTabla())
tabla.generarIndex()