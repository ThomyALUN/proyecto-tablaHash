class Nodo:
    def __init__(self, datosIniciales, apuntadorInicial=None):
        self.info=datosIniciales
        self.siguiente=apuntadorInicial
    def getInfo(self):
        return self.info
    def getSiguiente(self):
        return self.siguiente
    def setDatos(self, nuevosDatos):
        self.info=nuevosDatos
    def setSiguiente(self, nuevoApuntador):
        self.siguiente=nuevoApuntador