from funciones.general import *
from clases.claseListaEnlz import ListaNoOrd
from clases.monticuloBinario import *

class TablaHash:
    '''Clase tabla hash. Se encarga de manejar la tabla y todos los procesos relacionados:
    Ingresar datos, buscar datos, calcular las colisiones, etc...'''


    # Algoritmos de hashing:
        # 0: Módulo del tamaño
        # 1: Plegado
        # 2: Centro del cuadrado

    # Algoritmos para solución de colisiones:
        # 0: Prueba lineal (salto unitario)
        # 1: Rehashing (salto fijo)
        # 2: Sondeo cuadrático (salto cuadrático)
        # 3: Lista enlazada

    def __init__(self, tipo:int, longitud:int, tipoHash:int, tipoCol:int, ruta:str, grupDigMax:int=3, maxDigCent:int=2, paso:int=1):
        '''Método constructor. Sirve para inicializar varios de los parámetros clave de la clase'''
        # tipo: 0 -> Tabla con carga util
        # tipo: 1 -> Tabla de indexación
        self.tipo=tipo
        self.archivoCargado=False
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
        '''Cálcula el código hash usando el residuo (módulo) del tamaño'''
        ind=clave%self.tamanio
        return ind
    
    def hashPlegado(self, clave:int):
        '''Cálcula el código hash mediante el algoritmo de plegado'''
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
        '''Cálcula el código hash mediante el algoritmo del centro del cuadrado'''
        cuadrado=pow(clave, 2)
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
        return ind

    def calcularHash(self, clave:str):
        '''Se encarga de llamar el método de hashing para hallar el código de una clave según el método seleccionado inicialmente'''
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

    def ingresarDato(self, clave, cargaUtil):
        '''Se encarga de insertar un elemento si no fue encontrado en la posición designada por su código hash'''
        if self.tabla.count(None)==0 and self.colision!=3:
            raise IndexError("No se pueden ingresar más datos")
        ind=self.calcularHash(clave)
        if self.tabla[ind]==None:
            if self.colision!=3:
                self.tabla[ind]=[clave, cargaUtil]
            else:
                listaEn=ListaNoOrd()
                listaEn.agregarFrente(clave, cargaUtil)
                self.tabla[ind]=listaEn
        elif (self.colision in [0,1,2] and self.tabla[ind][0]==clave) or (self.colision==3 and self.tabla[ind].buscar(clave)):
            pass
        else:
            self.numCol+=1
            if self.colision==0:
                self.insPasoFijo(ind, clave, cargaUtil, 1) 
            elif self.colision==1:
                self.insPasoFijo(ind, clave, cargaUtil, self.paso)
            elif self.colision==2:
                self.insPasoCuad(ind, clave, cargaUtil)
            else:
                self.enlazar(ind, clave, cargaUtil)

    def buscarDato(self, clave):
        '''Se encarga de buscar un elemento en la tabla según el método de solución de colisiones seleccionado.
        Retorna None si no se encontró el elemento en la tabla.
        Retorna la información relacionada con la clave si fue encontrada en la tabla.'''
        ind=self.calcularHash(clave)
        self.pasosBus=1
        if self.tabla[ind]==None:
            cargaUtil=None
            pos=0
        elif self.colision!=3 and self.tabla[ind][0]==clave:
            cargaUtil=self.tabla[ind][1]
            pos=0
        else:
            if self.colision in [0,1,2]:
                if self.colision==0:
                    pos=self.busPasoFijo(ind, clave, 1) 
                elif self.colision==1:
                    pos=self.busPasoFijo(ind, clave, self.paso) 
                else:
                    pos=self.busPasoCuad(ind, clave)

                if pos==-1:
                    cargaUtil=None
                else:
                    cargaUtil=self.tabla[pos][1] 
            else:
                pos=self.busLista(ind, clave)
                if pos==-1:
                    cargaUtil=None
                else:
                    cargaUtil=self.tabla[ind].recuperarInfo(pos)
        if self.tipo==0 or pos==-1:
            return cargaUtil    # return None
        else:
            with open(self.ruta,"r", encoding="utf-8") as archivo:
                datos=archivo.readlines()
            linea=datos[cargaUtil-1].strip()
            info=linea.split(",")[1]
            return info

    def insPasoFijo(self, ind:int, clave:int, cargaUtil, paso:int):
        '''Introduce un elemento en la tabla hash realizando pasos constantes hacia 
        la derecha hasta encontrar un espacio vacío o recorrer toda la tabla'''
        for i in range(ind, (len(self.tabla))*paso+ind, paso):
            nuevoInd=i%len(self.tabla)
            if self.tabla[nuevoInd]==None:
                self.tabla[nuevoInd]=[clave, cargaUtil]
                break  
            elif self.tabla[nuevoInd][0]==clave:
                break

    def insPasoCuad(self, ind:int, clave:int, cargaUtil):
        '''Introduce un elemento en la tabla hash realizando pasos cuadráticos hacia 
        la derecha hasta encontrar un espacio vacío o recorrer toda la tabla'''
        posPosibles=[i for i in range(self.tamanio)]
        pos=0
        while len(posPosibles)>0:
            pos+=1
            if pos<10000:
                nuevoInd=(ind+pow(pos,2))%self.tamanio
            else:
                nuevoInd=(ind+pos)%self.tamanio
            if nuevoInd in posPosibles:
                if self.tabla[nuevoInd]==None:
                    self.tabla[nuevoInd]=[clave, cargaUtil]
                    break  
                elif self.tabla[nuevoInd][0]==clave:
                    break
                else:
                    posPosibles.remove(nuevoInd)

    def enlazar(self, ind:int, clave:int, cargaUtil):
        '''Permite enlazar un nuevo elemento a una lista enlazada que ya haya sido creada como parte de la tabla hash'''
        listaEn=self.tabla[ind]
        encontrado=listaEn.buscar(clave)
        if not encontrado:
            listaEn.agregarFinal(clave, cargaUtil)

    def busPasoFijo(self, ind:int, clave:int, paso:int):
        '''Realiza la búsqueda de un elemento realizando pasos del mismo tipo que el rehashing.
        Retorna la posición dónde se encontró o -1 si no se encontró'''
        for i in range(ind, (len(self.tabla))*paso+ind, paso):
            self.pasosBus+=1
            nuevoInd=i%len(self.tabla)
            if self.tabla[nuevoInd]==None:
                return -1
            elif self.tabla[nuevoInd][0]==clave:
                return nuevoInd
        return -1
    
    def busPasoCuad(self, ind:int, clave:int):
        '''Realiza la búsqueda de un elemento realizando pasos del mismo tipo que el sondeo cuadrático. 
        Retorna la posición dónde se encontró o -1 si no se encontró'''
        posPosibles=[i for i in range(self.tamanio)]
        pos=0
        while len(posPosibles)>0:
            self.pasosBus+=1
            pos+=1
            nuevoInd=(ind+pow(pos,2))%self.tamanio
            if nuevoInd in posPosibles:
                if self.tabla[nuevoInd]==None:
                    return -1
                elif self.tabla[nuevoInd][0]==clave:
                    return nuevoInd
                else:
                    posPosibles.remove(nuevoInd)
        return -1
    
    def busLista(self, ind:int, clave:int):
        '''Permite buscar un elemento en una lista enlazada que haga parte de la tabla hash'''
        listaEn=self.tabla[ind]
        subInd=listaEn.indice(clave)
        self.pasosBus+=subInd
        return subInd

    def generarIndex(self, ruta):
        '''Permite generar el archivo en disco con la tabla de indexación'''
        partesRuta=self.ruta.split(".")
        rutaFinal=ruta+".txt"
        with open(rutaFinal, "w") as archivo:
            mensaje=f"indexHash,{self.hashing},{self.colision}\n"
            archivo.write(mensaje)
            for linea in self.tabla:
                if linea!=None:
                    if self.colision in [0,1,2,]:
                        mensaje=f"{linea[0]},{linea[1]}\n"
                    else:
                        mensaje=""
                        for i in range(linea.tamanio()):
                            mensaje+=f"{linea.recuperarClave(i)},{linea.recuperarInfo(i)}"
                            if i<linea.tamanio()-1:
                                mensaje+=";"
                        mensaje+="\n"
                else:
                    mensaje="None,None\n"
                archivo.write(mensaje)

    def cargarIndex(self, rutaIndex:str):
        '''Permite cargar un archivo de indexación ya generado previamente y reconstruir la tabla hash a partir de este'''
        encabezado=False
        with open(rutaIndex, "r", encoding="utf-8") as archivo:
            datos=archivo.readlines()

        primeraLinea=datos[0].strip().split(",")
        if primeraLinea[0]=="indexHash":
            encabezado=True
            self.hashing=int(primeraLinea[1])
            self.colision=int(primeraLinea[2])
        else:
            # Si no tiene el encabezado, se asume hashing con módulo y colisiones con prueba lineal
            self.hashing=0
            self.colision=0

        if encabezado:
            inicio=1
            self.tamanio=len(datos)-1
        else:
            inicio=0
            self.tamanio=len(datos)

        tabla=[]
        for linea in datos[inicio:]:
            if self.colision!=3:
                valores=linea.strip().split(",")
                if valores[0]=="None":
                    tabla.append(None)
                else:
                    tabla.append([int(valores[0]),int(valores[1])])
            else:
                nodos=linea.strip().split(";")
                listaEn=ListaNoOrd()
                if nodos[0].split(",")[0]=="None":
                    tabla.append(None)
                else:
                    for nodo in nodos:
                        valores=nodo.strip().split(",")
                        listaEn.agregarFinal(int(valores[0]),int(valores[1]))
                    tabla.append(listaEn)
        self.tabla=tabla
        self.archivoCargado=True

    def generarMonticulo(self):
        '''Genera un montículo binario MIN para organizar las claves de menor a mayor'''
        if self.tabla:
            mont=MonticuloMin()
            
            for dato in self.tabla:
                if dato!=None:
                    if self.colision in [0,1,2]:
                        mont.insert(dato[0])
                    else:
                        for i in range(dato.tamanio()):
                            claveAct=dato.recuperarClave(i)
                            mont.insert(claveAct)
        self.mont=mont

    def obtenerPrimeros(self, cantidad):
        '''Utiliza la ordenación por el método del montículo para organizar los códigos de la tabla. 
        Luego busca los datos de los n primeros y los retorna'''
        vectorOrd=[]
        while self.mont.currentSize>0 and cantidad>0:
            clave=self.mont.delMin()
            datos=self.buscarDato(clave)
            vectorOrd.append([clave, datos])
            cantidad-=1
        return vectorOrd

    def setPaso(self, paso:int):
        '''Modifica el valor del paso para el método de hashing según el parámetro ingresado'''
        self.paso=paso

    def getTabla(self):
        '''Retorna la tabla (una lista)'''
        return self.tabla
    
    def getOcupacion(self):
        '''Retorna el factor de carga de la tabla hash'''
        return (self.tamanio - self.tabla.count(None))/self.tamanio
    
    def getColisiones(self):
        '''Retorna la cantidad de colisiones presentadas hasta el momento a la hora de ingresar nuevos datos en la tabla'''
        return self.numCol
    
    def getTamanio(self):
        '''Retorna el tamaño de la tabla hash'''
        return self.tamanio
    
    def __str__(self) -> str:
        '''Retorna una cadena si se imprime un objeto de la clase directamente'''
        datos="La tabla hash cuenta con los siguientes atributos:"
        datos+=f"\nTamaño: {self.getTamanio()}"
        datos+=f"\nOcupación: {self.getOcupacion()*100:.2f}%"
        if not self.archivoCargado:
            datos+=f"\nColisiones: {self.getColisiones()}"
        else:
            datos+=f"\nColisiones: - - -"
        return datos
    
if __name__=="__main__":
    tabla=TablaHash(11,0,3,"")
    lista=[54,26,93,17,77,31,44,55,20]
    for i,dato in enumerate(lista):
        tabla.ingresarDato(dato,i)
    print(tabla.getTabla())
    for dato in tabla.getTabla():
        print(dato)
