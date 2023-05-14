class HashTable:
    diccCol={
            0:"listaEnlz",
            1:"saltoUnit",
            2:"saltoFijo",
            3:"saltoCuad"
            }
    def __init__(self, longitud:int, tipoCol:int, ruta:str):
        self.tamanio=longitud
        self.tabla=[None]*longitud
        self.tablaIndex=[None]*longitud
        self.colision=self.diccCol[tipoCol]
        self.numCol=0

    def calcularHash(self, valor):
        ind=valor%self.tamanio
        return ind

    def ingresarDatos(self, valor):
        ind=self.calcularHash(valor)
        if self.tabla[ind]==None:
            self.tabla[ind]=valor
        else:
            self.numCol+=1
            self.pasoUnit(valor, ind)

    def pasoUnit(self, valor, ind:int):
        for i in range(ind, len(self.tabla)+ind):
            nuevoInd=i%len(self.tabla)
            if self.tabla[nuevoInd]==None:
                self.tabla[nuevoInd]=valor
                break                

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
