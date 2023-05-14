from funciones.general import *
from clases.claseListaEnlz import ListaNoOrd

class HashTable:

    # Algoritmos de hashing:
        # 0: Módulo del tamaño
        # 1: Plegado
        # 2: Centro del cuadrado

    # Algoritmos para solución de colisiones:
        # 0: Prueba lineal (salto unitario)
        # 1: Rehashing (salto fijo)
        # 2: Sondeo cuadrático (salto cuadrático)
        # 3: Lista enlazada

    def __init__(self, longitud:int, tipoHash:int, tipoCol:int, ruta:str, grupDigMax:int=3, maxDigCent:int=2, paso:int=1):
        self.tamanio=longitud
        self.tabla=[None]*longitud
        self.tablaIndex=[[None,None]]*longitud
        self.hashing=tipoHash
        self.colision=tipoCol
        self.grupDigMax=grupDigMax  # Indica la máxima cantidad de veces que se pliega un número
        self.maxDigCent=maxDigCent  # Indica la máxima cantidad de dígitos centrales que son tomados
        self.paso=paso
        self.numCol=0

    def hashResiduo(self, valor:int):
        ind=valor%self.tamanio
        return ind
    
    def hashPlegado(self, valor:int):
        cantDigitos=calcNumDigitos(valor)
        grupDig=cantDigitos/self.grupDigMax
        copiaValor=valor
        suma=0
        while copiaValor>=1:
            suma+=copiaValor%pow(10,grupDig)
            copiaValor//=pow(10,grupDig)
        ind=suma%self.tamanio
        return ind
    
    def hashCentro(self, valor:int):
        print(valor)
        cuadrado=pow(valor, 2)
        print(cuadrado)
        digCuad=calcNumDigitos(cuadrado)
        tomarAdelante=1
        while digCuad > 2:
            if tomarAdelante:
                cuadrado%=pow(10, digCuad-1)
                tomarAdelante=0
            else:
                cuadrado//=10
                tomarAdelante=1
            digCuad=calcNumDigitos(cuadrado)
        medio=cuadrado
        ind=medio%self.tamanio
        print(ind)
        return ind

    def calcularHash(self, valor:str):
        try:
            int(valor)
        except ValueError:
            valor=cad2NumPeso(valor)
        else:
            valor=int(valor)

        if self.hashing==0:
            ind=self.hashResiduo(valor)
        elif self.hashing==1:
            ind=self.hashPlegado(valor)
        else:
            ind=self.hashCentro(valor)
        return ind

    def ingresarDatos(self, valor):
        ind=self.calcularHash(valor)
        if self.tabla[ind]==valor:
            pass
        elif self.tabla[ind]==None:
            if self.colision!=3:
                self.tabla[ind]=valor
            else:
                listaEn=ListaNoOrd()
                listaEn.agregarFrente(valor)
                self.tabla[ind]=listaEn
        else:
            self.numCol+=1
            if self.colision==0:
                self.pasoFijo(valor, ind, 1) 
            elif self.colision==1:
                self.pasoFijo(valor, ind, self.paso)
            elif self.colision==2:
                self.pasoCuad(valor, ind)
            else:
                self.enlazar(valor, ind)

    def pasoFijo(self, valor:int, ind:int, paso:int):
        for i in range(ind, (len(self.tabla))*paso+ind, paso):
            nuevoInd=i%len(self.tabla)
            if self.tabla[nuevoInd]==valor:
                break
            elif self.tabla[nuevoInd]==None:
                self.tabla[nuevoInd]=valor
                break   

    def pasoCuad(self, valor:int, ind:int):
        posPosibles=[i for i in range(self.tamanio)]
        pos=0
        while len(posPosibles)>0:
            pos+=1
            nuevoInd=(ind+pow(pos,2))%self.tamanio
            if nuevoInd in posPosibles:
                if self.tabla[nuevoInd]==valor:
                    break
                elif self.tabla[nuevoInd]==None:
                    self.tabla[nuevoInd]=valor
                    break
                else:
                    posPosibles.remove(nuevoInd)

    def enlazar(self, valor:int, ind:int):
        listaEn=self.tabla[ind]
        encontrado=listaEn.buscar(valor)
        if not encontrado:
            listaEn.agregarFinal(valor)

    def setPaso(self, paso:int):
        self.paso=paso

    def getTabla(self):
        return self.tabla
    
    def getOcupacion(self):
        return (self.tamanio - self.tabla.count(None))/self.tamanio
    
    def getColisiones(self):
        return self.numCol
    
    def getTamanio(self):
        return self.tamanio
    
    def __str__(self) -> str:
        datos="La tabla hash cuenta con los siguientes atributos:"
        datos+=f"\nTamaño: {self.getTamanio()}"
        datos+=f"\nOcupación: {self.getOcupacion()*100:.2f}%"
        datos+=f"\nColisiones: {self.getColisiones()}"
        return datos
    
if __name__=="__main__":
    tabla=HashTable(11,0,3,"")
    lista=[54,26,93,17,77,31,44,55,20]
    for dato in lista:
        tabla.ingresarDatos(dato)
    print(tabla.getTabla())
    for dato in tabla.getTabla():
        print(dato)
