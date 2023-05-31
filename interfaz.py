import sys
import os
from PyQt5.QtWidgets import QWidget, QApplication, QMainWindow, QPushButton, QFileDialog,QVBoxLayout, QDialog, QListWidget, QTableWidget, QTableWidgetItem
from PyQt5.uic import loadUi
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from iconos import *
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtMultimedia import *
from PyQt5.QtMultimediaWidgets import *
from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QDesktopServices
from funciones.general import *
from tablaHash import TablaHash




class Inicio(QMainWindow):
    def __init__(self):
        super().__init__()
        self.widget_principal = loadUi("diseno_ui\diseno_inicio.ui", self)
        self.widget_size = self.widget_principal.size()
        self.cerrar.clicked.connect(self.exit)
        self.min.clicked.connect(self.minimizar)
        self.setWindowTitle('Ventana Inicio')
        self.frame.mouseMoveEvent = self.moveWindow
        self.BIniciar.clicked.connect(self.mostrarVentanaSubir)

    def moveWindow(self,e):
        if e.buttons() == Qt.LeftButton:
            self.move(self.pos()+e.globalPos()-self.clickPosition)
            self.clickPosition = e.globalPos()
            e.accept()
            
    def mousePressEvent(self, event):
        self.clickPosition = event.globalPos()        
    
    def keyPressEvent(self, qKeyEvent):
        if qKeyEvent.key() == QtCore.Qt.Key_Return:
            self.gui()

    def exit(self):
        app.exit()
        sys.exit()   
    
    def minimizar(self):        
        widget.showMinimized()

    def mostrarVentanaSubir(self):
        self.ventanaSubir = VentanaSubir()
        self.ventanaSubir.raise_()
        size = self.ventanaSubir.widget_size
        self.widget = QtWidgets.QStackedWidget()
        self.widget.addWidget(self.ventanaSubir)
        self.widget.setFixedSize(size)
        rec = app.desktop().screenGeometry()
        self.widget.move(int((rec.width() - self.widget.width()) / 2), 
                    int((rec.height() - self.widget.height()) / 2))
        
        self.widget.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.widget.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.widget.setGeometry(QtWidgets.QStyle.alignedRect(QtCore.Qt.LeftToRight, QtCore.Qt.AlignCenter, self.widget.size(), QtWidgets.qApp.desktop().availableGeometry()))
        self.ventanaSubir.show()
        self.widget.show()
        self.close()
        

class VentanaSubir(QMainWindow):
    def __init__(self):
        super().__init__()
        self.widget = loadUi("diseno_ui\diseno_subir.ui", self)
        self.widget_size = self.widget.size()
        self.setWindowTitle('Subir archivo')
        self.cerrar.clicked.connect(inicio.exit)
        self.min.clicked.connect(self.minimizar)
        self.frame.mouseMoveEvent = self.moveWindow
        self.BSubir.clicked.connect(self.seleccionarArchivo) 
           

    def seleccionarArchivo(self):
        dirPath = os.getcwd()  # Directorio de la carpeta actual
        # Buscar archivo.csv    
        ruta, _ = QFileDialog.getOpenFileName(self, "Buscar Archivo...", "C:\\","Archivos de Texto (*.txt);; Archivos CSV (*.csv);")
        try:                                                            # Se tiene un control sobre los problemas que se pueden presentar al intentar abrir el archivo o interactuar con él
            extension=ruta[-3:]                                         # Se obtiene la extensión del archivo
            if extension!="csv" and extension!="txt":
                if extension == "":
                    self.mensaje = (f"    No subió ningún archivo")
                    print(self.mensaje)
                    self.mostrarAdvertencia()
                else:
                    # Se comprueba que la exten1sión del archivo sea .csv
                    self.mensaje = (f"La extensión del archivo es inválida: {extension}")
                    print(self.mensaje)
                    self.mostrarAdvertencia()
            # src = cv2.imread(ruta, cv2.IMREAD_UNCHANGED) #Lee la ruta de la foto
            self.rutaArchivo = ruta
            self.datos=cargarDatos(self.rutaArchivo)
            print(self.datos)
            #self.controladorDf = ManejoDF(self.rutaCSV)
            #Devuelve la excepción que hay en ManejoDF
            #self.mensaje = self.controladorDf.leerCSV(ruta)
            self.mostrarVentana3()
        except FileNotFoundError:                                                         
            #Se detecta si han habido problemas a durante la carga o interacción con el archivo
            mensaje=f"El archivo: {ruta} no existe."
    
    def minimizar(self):
        inicio.widget.showMinimized()

    def moveWindow(self, e):
        if e.buttons() == Qt.LeftButton:
            self.move(self.pos() + e.globalPos() - self.clickPosition)
            self.clickPosition = e.globalPos()
            e.accept()

    def mousePressEvent(self, event):
        self.clickPosition = event.globalPos()
        
    def mostrarVentana3(self):
        self.ventana3 = Ventana3(self.datos, self.rutaArchivo)
        self.ventana3.raise_()
        size = self.ventana3.widget_size
        self.widget = QtWidgets.QStackedWidget()
        self.widget.addWidget(self.ventana3)
        self.widget.setFixedSize(size)
        rec = app.desktop().screenGeometry()
        self.widget.move(int((rec.width() - self.widget.width()) / 2), 
                    int((rec.height() - self.widget.height()) / 2))
        
        self.widget.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.widget.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.widget.setGeometry(QtWidgets.QStyle.alignedRect(QtCore.Qt.LeftToRight, QtCore.Qt.AlignCenter, self.widget.size(), QtWidgets.qApp.desktop().availableGeometry()))
        self.ventana3.show()
        self.widget.show()
        self.close()

    def mostrarAdvertencia(self):
        self.advertencia = Advertencia(self.mensaje)
        self.advertencia.show()
        
class Ventana3(QMainWindow):
    def __init__(self, datos, ruta):
        super().__init__()
        self.widget = loadUi("diseno_ui\diseno_ventana3.ui", self)
        self.widget_size = self.widget.size()
        self.setWindowTitle('ventana 3')
        self.cerrar.clicked.connect(inicio.exit)
        self.min.clicked.connect(self.minimizar)
        self.frame.mouseMoveEvent = self.moveWindow
        self.BSiguiente.clicked.connect(self.mostrarVentana4)
        self.datos = datos
        self.ruta = ruta
        self.tipoHash = {"modulo del tamaño": 0, "plegado":1, "centro del cuadrado": 2}
        self.tipoColisiones = {"prueba lineal": 0,"rehashing":1,"sondeo cuadrático":2,"encadenamiento":3}
        for tipo in self.tipoHash:
            print(tipo)
            self.comboBox.addItem(tipo)
        self.comboBox.setCurrentIndex(-1)
        
        for tipo in self.tipoColisiones:
            print(tipo)
            self.comboBox_2.addItem(tipo)
        self.comboBox_2.setCurrentIndex(-1)
        
    
    def minimizar(self):
        inicio.ventanaSubir.widget.showMinimized()

    def moveWindow(self, e):
        if e.buttons() == Qt.LeftButton:
            self.move(self.pos() + e.globalPos() - self.clickPosition)
            self.clickPosition = e.globalPos()
            e.accept()

    def mousePressEvent(self, event):
        self.clickPosition = event.globalPos()

    def mostrarAdvertencia(self):
        self.advertencia = Advertencia(self.mensaje)
        self.advertencia.show()
    
    def mostrarVentana4(self):
        try:
            tamanio = self.lineEdit.text()
            tamanio=int(tamanio)
            print(tamanio)
            if tamanio<len(self.datos):    
                self.mensaje = "Tamaño menor que los datos"
                self.mostrarAdvertencia()
                self.lineEdit.clear()
            else:
                hash = self.comboBox.currentText()
                valorHash = self.tipoHash[hash]
                colision = self.comboBox_2.currentText()
                valorColision = self.tipoColisiones[colision]
                tablaHash = TablaHash(1, tamanio, valorHash, valorColision,self.ruta)      
                tablaHash.setPaso(3)
                for i in range(len(self.datos)):
                    num=self.datos[i][0]
                    tablaHash.ingresarDato(int(num),i+1)
                print("")
                tabla = tablaHash.getTabla()
                print(tabla)
                print("")
                print(len(tabla))
                self.ventana4 = Ventana4(tablaHash, hash, colision)
                self.ventana4.raise_()
                size = self.ventana4.widget_size
                self.widget = QtWidgets.QStackedWidget()
                self.widget.addWidget(self.ventana4)
                self.widget.setFixedSize(size)
                rec = app.desktop().screenGeometry()
                self.widget.move(int((rec.width() - self.widget.width()) / 2), 
                            int((rec.height() - self.widget.height()) / 2))
                
                self.widget.setWindowFlag(QtCore.Qt.FramelessWindowHint)
                self.widget.setAttribute(QtCore.Qt.WA_TranslucentBackground)
                self.widget.setGeometry(QtWidgets.QStyle.alignedRect(QtCore.Qt.LeftToRight, QtCore.Qt.AlignCenter, self.widget.size(), QtWidgets.qApp.desktop().availableGeometry()))
                self.ventana4.show()
                self.widget.show()
                self.close()
                
        except ValueError:
            self.mensaje = "   El valor debe ser un número"
            self.mostrarAdvertencia()
            self.lineEdit.clear()
            print(len(self.datos))
    
    
class Ventana4(QMainWindow):
    def __init__(self,tabla, hash, colision):
        super().__init__()
        self.widget = loadUi("diseno_ui\diseno_ventana4.ui", self)
        self.widget_size = self.widget.size()
        self.setWindowTitle('ventana 4')
        self.cerrar.clicked.connect(inicio.exit)
        self.min.clicked.connect(self.minimizar)
        self.frame.mouseMoveEvent = self.moveWindow
        self.BSiguiente.clicked.connect(self.mostrarVentana5)
        self.BAtras.clicked.connect(self.mostrarVentana3)
        self.hashTable = tabla
        self.matriz = self.hashTable.getTabla()
        self.tamanio = self.hashTable.getTamanio()
        self.tipoHash = hash        
        self.tipoColision = colision
        self.colisiones = self.hashTable.getColisiones()
        self.factorCarga = round(self.hashTable.getOcupacion()*100, 2)
        self.tableWidget.setRowCount(self.tamanio)
        self.labelTamanio.setText(str(self.tamanio))
        self.labelHashing.setText(self.tipoHash)
        self.labelMetodoColisiones.setText(self.tipoColision)
        self.labelColisiones.setText(str(self.colisiones))
        self.labelFactorCarga.setText(str(self.factorCarga)+"%")
        if self.tipoColision == "encadenamiento":
            self.tableWidget.cellClicked.connect(self.mostrarListaEnlazada)
        
        
        for i in range(self.tamanio):
            if self.matriz[i] == None:
                item = QTableWidgetItem(str("None"))
                item_2 = QTableWidgetItem(str("None"))
                self.tableWidget.setItem(i, 0, item)
                self.tableWidget.setItem(i, 1, item_2)
            else:
                if self.tipoColision == "encadenamiento":
                    if self.matriz[i].tamanio()== 1:
                        valor = self.matriz[i].getCabeza()
                        item = QTableWidgetItem(str(valor.getClave()))
                        item_2 = QTableWidgetItem(str(valor.getInfo()))
                        self.tableWidget.setItem(i, 0, item)
                        self.tableWidget.setItem(i, 1, item_2)
                    else:
                        item = QTableWidgetItem(str("Lista"))
                        item_2 = QTableWidgetItem(str("Enlazada"))
                        self.tableWidget.setItem(i, 0, item)
                        self.tableWidget.setItem(i, 1, item_2)
                    
                else:
                    for j in range(2):
                        item = QTableWidgetItem(str(self.matriz[i][j]))
                        self.tableWidget.setItem(i, j, item)
                
    def mostrarListaEnlazada(self, row, col):
        if self.matriz[row] != None:
            clave = self.matriz[row].getCabeza().getClave()
            lista = self.hashTable.obtenerListaEn(clave)
            self.listaEnlazada = ListaEnlazada(lista)
            self.listaEnlazada.show()
    
    def minimizar(self):
        inicio.ventanaSubir.ventana3.widget.showMinimized()

    def moveWindow(self, e):
        if e.buttons() == Qt.LeftButton:
            self.move(self.pos() + e.globalPos() - self.clickPosition)
            self.clickPosition = e.globalPos()
            e.accept()

    def mousePressEvent(self, event):
        self.clickPosition = event.globalPos()

    def mostrarAdvertencia(self):
        self.advertencia = Advertencia(self.mensaje)
        self.advertencia.show()
    
    def mostrarVentana3(self):
        self.ventana3 = Ventana3()
        self.ventana3.raise_()
        size = self.ventana3.widget_size
        self.widget = QtWidgets.QStackedWidget()
        self.widget.addWidget(self.ventana3)
        self.widget.setFixedSize(size)
        rec = app.desktop().screenGeometry()
        self.widget.move(int((rec.width() - self.widget.width()) / 2), 
                    int((rec.height() - self.widget.height()) / 2))
        
        self.widget.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.widget.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.widget.setGeometry(QtWidgets.QStyle.alignedRect(QtCore.Qt.LeftToRight, QtCore.Qt.AlignCenter, self.widget.size(), QtWidgets.qApp.desktop().availableGeometry()))
        self.ventana3.show()
        self.widget.show()
        self.close()
        
    def mostrarVentana5(self):
        self.ventana5 = Ventana5(self.hashTable)
        self.ventana5.raise_()
        size = self.ventana5.widget_size
        self.widget = QtWidgets.QStackedWidget()
        self.widget.addWidget(self.ventana5)
        self.widget.setFixedSize(size)
        rec = app.desktop().screenGeometry()
        self.widget.move(int((rec.width() - self.widget.width()) / 2), 
                    int((rec.height() - self.widget.height()) / 2))
        
        self.widget.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.widget.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.widget.setGeometry(QtWidgets.QStyle.alignedRect(QtCore.Qt.LeftToRight, QtCore.Qt.AlignCenter, self.widget.size(), QtWidgets.qApp.desktop().availableGeometry()))
        self.ventana5.show()
        self.widget.show()
        self.close()
    
    
        
class Ventana5(QMainWindow):
    def __init__(self,tabla):
        super().__init__()
        self.widget = loadUi("diseno_ui\diseno_ventana5.ui", self)
        self.widget_size = self.widget.size()
        self.setWindowTitle('ventana 5')
        self.cerrar.clicked.connect(inicio.exit)
        self.min.clicked.connect(self.minimizar)
        self.frame.mouseMoveEvent = self.moveWindow
        self.BSiguiente.clicked.connect(self.mostrarVentana6)
        self.BAtras.clicked.connect(self.mostrarVentana3)
        self.hashTable = tabla
        self.matriz = self.hashTable.obtenerPrimeros(10)
        for i in range(10):
            for j in range(2):
                item = QTableWidgetItem(str(self.matriz[i][j]))
                self.tableWidget.setItem(i, j, item)
            
    
    def minimizar(self):
        inicio.ventanaSubir.ventana3.widget.showMinimized()

    def moveWindow(self, e):
        if e.buttons() == Qt.LeftButton:
            self.move(self.pos() + e.globalPos() - self.clickPosition)
            self.clickPosition = e.globalPos()
            e.accept()

    def mousePressEvent(self, event):
        self.clickPosition = event.globalPos()

    def mostrarAdvertencia(self):
        self.advertencia = Advertencia(self.mensaje)
        self.advertencia.show()
    
    def mostrarVentana3(self):
        self.ventana3 = Ventana3()
        self.ventana3.raise_()
        size = self.ventana3.widget_size
        self.widget = QtWidgets.QStackedWidget()
        self.widget.addWidget(self.ventana3)
        self.widget.setFixedSize(size)
        rec = app.desktop().screenGeometry()
        self.widget.move(int((rec.width() - self.widget.width()) / 2), 
                    int((rec.height() - self.widget.height()) / 2))
        
        self.widget.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.widget.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.widget.setGeometry(QtWidgets.QStyle.alignedRect(QtCore.Qt.LeftToRight, QtCore.Qt.AlignCenter, self.widget.size(), QtWidgets.qApp.desktop().availableGeometry()))
        self.ventana3.show()
        self.widget.show()
        self.close()   
        
    def mostrarVentana6(self):
        self.ventana6 = Ventana6(self.hashTable)
        self.ventana6.raise_()
        size = self.ventana6.widget_size
        self.widget = QtWidgets.QStackedWidget()
        self.widget.addWidget(self.ventana6)
        self.widget.setFixedSize(size)
        rec = app.desktop().screenGeometry()
        self.widget.move(int((rec.width() - self.widget.width()) / 2), 
                    int((rec.height() - self.widget.height()) / 2))
        
        self.widget.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.widget.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.widget.setGeometry(QtWidgets.QStyle.alignedRect(QtCore.Qt.LeftToRight, QtCore.Qt.AlignCenter, self.widget.size(), QtWidgets.qApp.desktop().availableGeometry()))
        self.ventana6.show()
        self.widget.show()
        self.close()
        
class Ventana6(QMainWindow):
    def __init__(self,tabla):
        super().__init__()
        self.widget = loadUi("diseno_ui\diseno_ventana6.ui", self)
        self.widget_size = self.widget.size()
        self.setWindowTitle('ventana 6')
        self.cerrar.clicked.connect(inicio.exit)
        self.min.clicked.connect(self.minimizar)
        self.frame.mouseMoveEvent = self.moveWindow
        self.BSiguiente.clicked.connect(self.mostrarVentana7)
        #self.BAtras.clicked.connect(self.mostrarVentana3)
        self.hashTable = tabla
        self.BBuscar.clicked.connect(self.buscarDato)
        
    def buscarDato(self):
        self.clave = int(self.lineEdit.text())
        nombre = self.hashTable.buscarDato(self.clave)
        print(nombre)
        self.mostrarConfirmacion(nombre)
        
    def minimizar(self):
        inicio.ventanaSubir.ventana3.widget.showMinimized()

    def moveWindow(self, e):
        if e.buttons() == Qt.LeftButton:
            self.move(self.pos() + e.globalPos() - self.clickPosition)
            self.clickPosition = e.globalPos()
            e.accept()

    def mousePressEvent(self, event):
        self.clickPosition = event.globalPos()

    def mostrarAdvertencia(self):
        self.advertencia = Advertencia(self.mensaje)
        self.advertencia.show()
    
    def mostrarVentana3(self):
        self.ventana3 = Ventana3()
        self.ventana3.raise_()
        size = self.ventana3.widget_size
        self.widget = QtWidgets.QStackedWidget()
        self.widget.addWidget(self.ventana3)
        self.widget.setFixedSize(size)
        rec = app.desktop().screenGeometry()
        self.widget.move(int((rec.width() - self.widget.width()) / 2), 
                    int((rec.height() - self.widget.height()) / 2))
        
        self.widget.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.widget.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.widget.setGeometry(QtWidgets.QStyle.alignedRect(QtCore.Qt.LeftToRight, QtCore.Qt.AlignCenter, self.widget.size(), QtWidgets.qApp.desktop().availableGeometry()))
        self.ventana3.show()
        self.widget.show()
        self.close()
        
    def mostrarVentana7(self):
        self.ventana7 = Ventana7(self.hashTable)
        self.ventana7.raise_()
        size = self.ventana7.widget_size
        self.widget = QtWidgets.QStackedWidget()
        self.widget.addWidget(self.ventana7)
        self.widget.setFixedSize(size)
        rec = app.desktop().screenGeometry()
        self.widget.move(int((rec.width() - self.widget.width()) / 2), 
                    int((rec.height() - self.widget.height()) / 2))
        
        self.widget.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.widget.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.widget.setGeometry(QtWidgets.QStyle.alignedRect(QtCore.Qt.LeftToRight, QtCore.Qt.AlignCenter, self.widget.size(), QtWidgets.qApp.desktop().availableGeometry()))
        self.ventana7.show()
        self.widget.show()
        self.close()
        
    def mostrarConfirmacion(self, mensaje):
        self.confirmacion = Confirmacion(mensaje)
        self.confirmacion.show()      

class Ventana7(QMainWindow):
    def __init__(self,tabla):
        super().__init__()
        self.widget = loadUi("diseno_ui\exportar.ui", self)
        self.widget_size = self.widget.size()
        self.setWindowTitle('ventana exportar')
        self.cerrar.clicked.connect(inicio.exit)
        self.min.clicked.connect(self.minimizar)
        self.frame.mouseMoveEvent = self.moveWindow
        #self.BSiguiente.clicked.connect(self.mostrarVentana5)
        #self.BAtras.clicked.connect(self.mostrarVentana3)
        self.hashTable = tabla
        self.BExportar.clicked.connect(self.exportarArchivo)
        
    def exportarArchivo(self):
        file_path = QFileDialog.getExistingDirectory(self, "Seleccionar carpeta donde guardar archivo")
        if file_path:
            nombre_archivo = 'ArchNombres1Index'
            ruta_guardado = os.path.join(file_path, nombre_archivo)
            self.hashTable.generarIndex(ruta_guardado)
        else:
            mensaje = "No se seleccionó ninguna carpeta"
            self.advertencia = Advertencia(mensaje) 
            self.advertencia.show()    
        
        #self.mostrarConfirmacion(nombre)
        
    def minimizar(self):
        inicio.ventanaSubir.ventana3.widget.showMinimized()

    def moveWindow(self, e):
        if e.buttons() == Qt.LeftButton:
            self.move(self.pos() + e.globalPos() - self.clickPosition)
            self.clickPosition = e.globalPos()
            e.accept()

    def mousePressEvent(self, event):
        self.clickPosition = event.globalPos()

    def mostrarAdvertencia(self):
        self.advertencia = Advertencia(self.mensaje)
        self.advertencia.show()
    
    def mostrarVentana3(self):
        self.ventana3 = Ventana3()
        self.ventana3.raise_()
        size = self.ventana3.widget_size
        self.widget = QtWidgets.QStackedWidget()
        self.widget.addWidget(self.ventana3)
        self.widget.setFixedSize(size)
        rec = app.desktop().screenGeometry()
        self.widget.move(int((rec.width() - self.widget.width()) / 2), 
                    int((rec.height() - self.widget.height()) / 2))
        
        self.widget.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.widget.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.widget.setGeometry(QtWidgets.QStyle.alignedRect(QtCore.Qt.LeftToRight, QtCore.Qt.AlignCenter, self.widget.size(), QtWidgets.qApp.desktop().availableGeometry()))
        self.ventana3.show()
        self.widget.show()
        self.close()
        
    def mostrarConfirmacion(self, mensaje):
        self.confirmacion = Confirmacion(mensaje)
        self.confirmacion.show()   

class ListaEnlazada(QDialog):
    def __init__(self,lista):
        super(ListaEnlazada,self).__init__()
        loadUi("diseno_ui/diseno_lista.ui", self)
        self.cerrar.clicked.connect(self.ocultar)
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.widget.mouseMoveEvent = self.moveWindow
        self.lista = lista
        for i in range(len(lista)):
            for j in range(2):
                item = QTableWidgetItem(str(self.lista[i][j]))
                self.tableWidget.setItem(i, j, item)
            
    def moveWindow(self,e):
        if e.buttons() == Qt.LeftButton:
            self.move(self.pos()+e.globalPos()-self.clickPosition)
            self.clickPosition = e.globalPos()
            e.accept()
                
    def mousePressEvent(self, event):
        self.clickPosition = event.globalPos()
    
    def keyPressEvent(self, qKeyEvent):
        if qKeyEvent.key() == QtCore.Qt.Key_Return:
            self.gui()
    def minimizar(self):
        self.widget.showMinimized()
    def ocultar(self):
        self.close()


class Advertencia(QDialog):
    def __init__(self,mensaje):
        super(Advertencia,self).__init__()
        loadUi("diseno_ui/advertencia.ui", self)
        self.cerrar_5.clicked.connect(self.ocultar)
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.widget.mouseMoveEvent = self.moveWindow
        self.label_6.setText(mensaje)

    def moveWindow(self,e):
        if e.buttons() == Qt.LeftButton:
            self.move(self.pos()+e.globalPos()-self.clickPosition)
            self.clickPosition = e.globalPos()
            e.accept()
                
    def mousePressEvent(self, event):
        self.clickPosition = event.globalPos()
    
    def keyPressEvent(self, qKeyEvent):
        if qKeyEvent.key() == QtCore.Qt.Key_Return:
            self.gui()

    def ocultar(self):
        self.close()
        
class Confirmacion(QDialog):
    def __init__(self,mensaje):
        super(Confirmacion,self).__init__()
        loadUi("diseno_ui/confirmacion.ui", self)
        self.cerrar_6.clicked.connect(self.ocultar)
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.widget.mouseMoveEvent = self.moveWindow
        self.label_2.setText(mensaje)

    def moveWindow(self,e):
        if e.buttons() == Qt.LeftButton:
            self.move(self.pos()+e.globalPos()-self.clickPosition)
            self.clickPosition = e.globalPos()
            e.accept()
                
    def mousePressEvent(self, event):
        self.clickPosition = event.globalPos()
    
    def keyPressEvent(self, qKeyEvent):
        if qKeyEvent.key() == QtCore.Qt.Key_Return:
            self.gui()

    def ocultar(self):
        self.close()
    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    inicio = Inicio()
    size = inicio.widget_size
    widget = QtWidgets.QStackedWidget()

    widget.addWidget(inicio)
    widget.setFixedSize(size)
    
    rec = app.desktop().screenGeometry()
    widget.move(int((rec.width() - widget.width()) / 2), 
                int((rec.height() - widget.height()) / 2))
    widget.setWindowFlag(QtCore.Qt.FramelessWindowHint)
    widget.setAttribute(QtCore.Qt.WA_TranslucentBackground)
    widget.setGeometry(QtWidgets.QStyle.alignedRect(QtCore.Qt.LeftToRight, QtCore.Qt.AlignCenter, widget.size(), QtWidgets.qApp.desktop().availableGeometry()))
    widget.show()
    
    inicio.show()
    sys.exit(app.exec_())