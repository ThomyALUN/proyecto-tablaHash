class Nodo:
    def __init__(self, clave, datosIniciales, apuntadorInicial=None):
        self.clave=clave
        self.info=datosIniciales
        self.siguiente=apuntadorInicial
    def getClave(self):
        return self.clave
    def getInfo(self):
        return self.info
    def getSiguiente(self):
        return self.siguiente
    def setDatos(self, nuevosDatos):
        self.info=nuevosDatos
    def setSiguiente(self, nuevoApuntador):
        self.siguiente=nuevoApuntador