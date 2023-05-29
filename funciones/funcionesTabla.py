from tablaHash import TablaHash
from funciones.general import cargarDatos

def crearTabla(ruta, tamanio, hashing, colisiones, paso=2):
    datos=cargarDatos(ruta)
    tabla=TablaHash(1, tamanio, hashing, colisiones, ruta)
    if hashing==1:
        tabla.setPaso(paso)
    for i in range(len(datos)):
        num=datos[i][0]
        tabla.ingresarDato(int(num),i+1)
    return tabla

def longitudDatos(ruta):
    return len(cargarDatos(ruta))
