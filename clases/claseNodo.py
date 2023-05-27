class Nodo:
    '''Clase Nodo. Cada nodo almacena una clave, una carga util o información y un apuntador'''
    def __init__(self, clave, datosIniciales, apuntadorInicial=None):
        '''Método constructor: Crea el nodo con los parámetros básicos mínimos'''
        self.clave=clave
        self.info=datosIniciales
        self.siguiente=apuntadorInicial
    def getClave(self):
        '''Retorna la clave del nodo'''
        return self.clave
    def getInfo(self):
        '''Retorna la carga útil del nodo'''
        return self.info
    def getSiguiente(self):
        '''Retorna el valor hacia el cual apunta el nodo. Puede ser None u otro objeto de la clase Nodo'''
        return self.siguiente
    def setDatos(self, nuevosDatos):
        '''Sobreescribe la carga útil del nodo con el valor ingresado como parámetro'''
        self.info=nuevosDatos
    def setSiguiente(self, nuevoApuntador):
        '''Sobreescribe lel apuntador del nodo con el valor ingresado como parámetro'''
        self.siguiente=nuevoApuntador