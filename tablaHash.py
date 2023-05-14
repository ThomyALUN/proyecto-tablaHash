from funciones.general import *
from clases.claseListaEnlz import ListaNoOrd

class TablaHash:

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
        self.hashing=tipoHash
        self.colision=tipoCol
        self.ruta=ruta
        self.grupDigMax=grupDigMax  # Indica la máxima cantidad de veces que se pliega un número
        self.maxDigCent=maxDigCent  # Indica la máxima cantidad de dígitos centrales que son tomados
        self.paso=paso
        self.numCol=0

    def hashResiduo(self, clave:int):
        ind=clave%self.tamanio
        return ind
    
    def hashPlegado(self, clave:int):
        cantDigitos=calcNumDigitos(clave)
        grupDig=cantDigitos/self.grupDigMax
        copiaclave=clave
        suma=0
        while copiaclave>=1:
            suma+=copiaclave%pow(10,grupDig)
            copiaclave//=pow(10,grupDig)
        ind=suma%self.tamanio
        return ind
    
    def hashCentro(self, clave:int):
        print(clave)
        cuadrado=pow(clave, 2)
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

    def calcularHash(self, clave:str):
        try:
            int(clave)
        except ValueError:
            clave=cad2NumPeso(clave)
        else:
            clave=int(clave)

        if self.hashing==0:
            ind=self.hashResiduo(clave)
        elif self.hashing==1:
            ind=self.hashPlegado(clave)
        else:
            ind=self.hashCentro(clave)
        return ind

    def ingresarDatos(self, clave, cargaUtil):
        ind=self.calcularHash(clave)
        if self.tabla[ind]==clave:
            pass
        elif self.tabla[ind]==None:
            if self.colision!=3:
                self.tabla[ind]=[clave, cargaUtil]
            else:
                listaEn=ListaNoOrd()
                listaEn.agregarFrente(clave, cargaUtil)
                self.tabla[ind]=listaEn
        else:
            self.numCol+=1
            if self.colision==0:
                self.pasoFijo(ind, clave, cargaUtil, 1) 
            elif self.colision==1:
                self.pasoFijo(ind, clave, cargaUtil, self.paso)
            elif self.colision==2:
                self.pasoCuad(ind, clave, cargaUtil)
            else:
                self.enlazar(ind, clave, cargaUtil)

    def pasoFijo(self, ind:int, clave:int, cargaUtil, paso:int):
        for i in range(ind, (len(self.tabla))*paso+ind, paso):
            nuevoInd=i%len(self.tabla)
            if self.tabla[nuevoInd]==None:
                self.tabla[nuevoInd]=[clave, cargaUtil]
                break  
            elif self.tabla[nuevoInd][0]==clave:
                break

    def pasoCuad(self, ind:int, clave:int, cargaUtil):
        posPosibles=[i for i in range(self.tamanio)]
        pos=0
        while len(posPosibles)>0:
            pos+=1
            nuevoInd=(ind+pow(pos,2))%self.tamanio
            if nuevoInd in posPosibles:
                if self.tabla[nuevoInd]==None:
                    self.tabla[nuevoInd]=[clave, cargaUtil]
                    break  
                elif self.tabla[nuevoInd][0]==clave:
                    break
                else:
                    posPosibles.remove(nuevoInd)

    def enlazar(self, ind:int, clave:int, cargaUtil):
        listaEn=self.tabla[ind]
        encontrado=listaEn.buscar(clave)
        if not encontrado:
            listaEn.agregarFinal(clave, cargaUtil)

    def generarIndex(self):
        partesRuta=self.ruta.split(".")
        rutaSinFmt=partesRuta[0]
        formato=partesRuta[1]
        rutaFinal=rutaSinFmt+"Index"+"."+formato
        with open(rutaFinal, "w") as archivo:
            for linea in self.tabla:
                if linea!=None:
                    mensaje=f"{linea[0]}, {linea[1]}\n"
                else:
                    mensaje="None, None\n"
                archivo.write(mensaje)

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
    tabla=TablaHash(11,0,3,"")
    lista=[54,26,93,17,77,31,44,55,20]
    for i,dato in enumerate(lista):
        tabla.ingresarDatos(dato,i)
    print(tabla.getTabla())
    for dato in tabla.getTabla():
        print(dato)
