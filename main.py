from funciones.funcionesTabla import *

ruta = "ArchNombres1.txt"

while True:
    try:
        tamanio=input("Ingrese el tamaño de la tabla: ")
        tamanio=int(tamanio)
    except ValueError:
        print("El valor debe ser un número")
    else:
        if tamanio<longitudDatos(ruta):
            print("El tamaño no puede ser menor que la cantidad de datos")
        else:
            break

tabla=crearTabla(ruta, tamanio, 1, 3)
print("")
print(tabla)
print("")
print(tabla.getTabla())
tabla.generarIndex("ArchNombres1Index")
print(tabla.buscarDato(990))

print("")
tabla.cargarIndex("ArchNombres1Index.txt")  
print(tabla.buscarDato(990))
print("")
print(tabla)
print("")
print(tabla.getTabla())
print(tabla.obtenerPrimeros(5))
if tabla.colision==3:
    print(tabla.obtenerListaEn(709))