class MonticuloMin:
    def __init__(self):
        self.heapList = [0]
        self.currentSize = 0

    # Inserta elemento en el montículo
    def insert(self, k):
        self.heapList.append(k)
        self.currentSize = self.currentSize + 1
        self.percUp(self.currentSize)

    # Filtrado hacia arriba
    def percUp(self, posHijo):
        while posHijo // 2 > 0:
            posPadre = posHijo // 2
            if self.heapList[posHijo] < self.heapList[posPadre]:
                temp = self.heapList[posPadre]
                self.heapList[posPadre] = self.heapList[posHijo]
                self.heapList[posHijo] = temp
            posHijo = posPadre

    # Devuelve y elimina el menor valor de montículo (raíz)
    def delMin(self):
        retVal = self.heapList[1]
        self.heapList[1] = self.heapList[self.currentSize]
        self.currentSize = self.currentSize - 1
        self.heapList.pop()
        self.percDown(1)
        return retVal

    # Filtrado hacia abajo
    def percDown(self, i):
        while (i * 2 ) <= self.currentSize:
            mc = self.minChild(i)
            if self.heapList[i] > self.heapList[mc]:
                temp = self.heapList[i]
                self.heapList[i] = self.heapList[mc]
                self.heapList[mc] = temp
            i = mc

    # Calcula el posHijo de menor valor
    def minChild(self, i):
        if i * 2 + 1 > self.currentSize:
            return i * 2
        else:
            if self.heapList[i*2] < self.heapList[i*2 + 1]:
                return i * 2
            else:
                return i * 2 + 1     

class MonticuloMax:
    def __init__(self) -> None:
        pass