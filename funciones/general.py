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