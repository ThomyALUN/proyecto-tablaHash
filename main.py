from funciones.general import *
from tablaHash import HashTable

archivo = "ArchNombres1.txt"

with open(archivo, "r", encoding="utf-8") as archivo:
    datos=archivo.readlines()

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

tabla=HashTable(tamanio, 2, 1, "")
tabla.setPaso(3)
for i in range(len(datos)):
    num=datos[i].strip().split(",")[0]
    tabla.ingresarDatos(int(num))
print("")
print(tabla)
print("")
print(tabla.getTabla())