from clases.claseNodo import Nodo

class ListaNoOrd:
    def __init__(self):
        self.cabeza=None

    def estaVacia(self):
        return self.cabeza==None
    
    def agregarFrente(self, clave, item):
        '''Crea un nuevo nodo y crea un enlace con la cabeza actual de la lista.
        Luego pone el nuevo nodo como la nueva cabeza de la lista, es decir, desplaza la cabeza anterior'''
        nuevo=Nodo(clave, item)
        nuevo.setSiguiente(self.cabeza)
        self.cabeza=nuevo

    def agregarFinal(self, clave, item):
        self.insertar(clave, item, self.tamanio())

    def getCabeza(self):
        return self.cabeza
    
    def recorrer(self):
        cadena=""
        actual=self.cabeza
        while actual!=None:
            if actual.getSiguiente()==None:
                cadena+=f"{actual.getClave()}: {actual.getInfo()}"
            else:
                cadena+=f"{actual.getClave()}: {actual.getInfo()}, "
            actual=actual.getSiguiente()
        return cadena

    def tamanio(self):
        i=0
        actual=self.cabeza
        while actual!=None:
            i+=1
            actual=actual.getSiguiente()
        return i
    
    def buscar(self, clave):
        '''Busca una clave y retorna True al encontrarla o False si no esta en la lista'''
        actual=self.cabeza
        while actual!=None:
            if actual.getClave()==clave:
                return True
            actual=actual.getSiguiente()
        return False
    
    def insertar(self, clave, item, pos):
        '''Agrega un elemento en la posición indicada. 
        Recibe los datos o carga útil del elemento y la posición en la que se desea introducir.
        la posición de los elementos actuales va de 0 hasta n - 1, 
        siendo n la cantidad de elementos presentes actualmente en el arreglo.
        Sin embargo, el método recibe valores de posición entre 0 y n, 
        debido a que la posición n permite añadir elementos al final de la lista enlazada.
        '''
        tamanio=self.tamanio()
        if pos<0: 
            if abs(pos)<=tamanio:  
                pos%=tamanio    # Permite utilizar índices negativos
            else:
                raise IndexError("Índice fuera del rango de la lista actual")
        if pos==0:
            self.agregarFrente(clave, item)
        else:
            if tamanio<pos:
                raise IndexError("Índice fuera del rango de la lista actual")
            else:
                if pos<0: 
                    pos%=tamanio    # Permite utilizar índices negativos
                nuevo=Nodo(clave, item)
                previo=None
                actual=self.cabeza
                for i in range(pos+1):
                    if i==pos:
                        nuevo.setSiguiente(actual)
                        previo.setSiguiente(nuevo)
                    else:
                        previo=actual
                        actual=actual.getSiguiente()

    def eliminar(self, pos=-1):
        '''Elimina el elemento (nodo) en la posición indicada y retorna sus datos'''
        tamanio=self.tamanio()
        if pos<0: 
            if abs(pos)<=tamanio:  
                pos%=tamanio    # Permite utilizar índices negativos
            else:
                raise IndexError("Índice fuera del rango de la lista actual")
        if pos==0:
            actual=self.cabeza
            self.cabeza=self.cabeza.getSiguiente()
            return actual.getInfo()
        else:
            if tamanio-1<pos or tamanio<pos%tamanio:
                raise IndexError("Índice fuera del rango de la lista actual")
            else:
                previo=None
                actual=self.cabeza
                for i in range(pos+1):
                    if i==pos:
                        previo.setSiguiente(actual.getSiguiente())
                        return actual.getInfo()
                    else:
                        previo=actual
                        actual=actual.getSiguiente()
        
    def contar(self, dato):
        '''Cuenta la cantidad de veces que un dato fue hallado como
        la carga útil de un nodo en la lista enlazada'''
        veces=0
        actual=self.cabeza
        while actual!=None:
            if actual.getInfo()==dato:
                veces+=1
            actual=actual.getSiguiente()
        return veces
    
    def remover(self, dato):
        '''Elimina el primer elemento encontrado cuya carga útil sea el dato
        recibido como parámetro'''
        previo=None
        actual=self.cabeza
        while actual!=None:
            if actual.getInfo()==dato:
                if self.cabeza==actual:
                    self.cabeza=actual.getSiguiente()
                else:
                    previo.setSiguiente(actual.getSiguiente())
                return None
            else:
                previo=actual
                actual=actual.getSiguiente()
        raise ValueError("El valor ingresado para remover no ha sido encontrado")
    
    def __str__(self) -> str:
        return self.recorrer()