def calcNumDigitos(num:int):
    cantDigitos=0
    while num>=1:
        num=num//10
        cantDigitos+=1
    return cantDigitos

def cad2NumPeso(cad:str):
    suma=0
    for i, car in enumerate(cad):
        suma+=(i+1)*ord(car)
    return suma

def cargarDatos(ruta:str, separador:str=","):
    with open(ruta,"r", encoding="utf-8") as archivo:
        datos=archivo.readlines()
    for i, linea in enumerate(datos):
        datos[i]=linea.strip().split(separador)
    return datos

