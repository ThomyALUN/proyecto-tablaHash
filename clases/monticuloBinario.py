class MonticuloMin:
    '''Clase monticulo binario MIN. Solo maneja claves, es decir, no almacena ninguna carga útil relacionada a las claves'''
    def __init__(self):
        '''Método constructor: Inicia la lista y el párametro de control del tamaño'''
        self.heapList = [0]
        self.currentSize = 0

    def insert(self, k):
        '''Inserta un elemento en el montículo'''
        self.heapList.append(k)
        self.currentSize = self.currentSize + 1
        self.percUp(self.currentSize)

    def percUp(self, posHijo):
        '''Filtrado hacia arriba'''
        while posHijo // 2 > 0:
            posPadre = posHijo // 2
            if self.heapList[posHijo] < self.heapList[posPadre]:
                temp = self.heapList[posPadre]
                self.heapList[posPadre] = self.heapList[posHijo]
                self.heapList[posHijo] = temp
            posHijo = posPadre

    def delMin(self):
        '''Elimina y retorna el menor valor de montículo (raíz)'''
        retVal = self.heapList[1]
        self.heapList[1] = self.heapList[self.currentSize]
        self.currentSize = self.currentSize - 1
        self.heapList.pop()
        self.percDown(1)
        return retVal

    def percDown(self, i):
        '''Filtrado hacia abajo'''
        while (i * 2 ) <= self.currentSize:
            mc = self.minChild(i)
            if self.heapList[i] > self.heapList[mc]:
                temp = self.heapList[i]
                self.heapList[i] = self.heapList[mc]
                self.heapList[mc] = temp
            i = mc

    def minChild(self, i):
        '''Calcula y retorna la posicion del hijo de menor valor según un padre dado'''
        if i * 2 + 1 > self.currentSize:
            return i * 2
        else:
            if self.heapList[i*2] < self.heapList[i*2 + 1]:
                return i * 2
            else:
                return i * 2 + 1     