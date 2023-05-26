import sys
import os
from PyQt5.QtWidgets import QWidget, QApplication, QMainWindow, QPushButton, QFileDialog,QVBoxLayout, QDialog, QListWidget
from PyQt5.uic import loadUi
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from iconos import *
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtMultimedia import *
from PyQt5.QtMultimediaWidgets import *
from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QDesktopServices



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
        ruta, _ = QFileDialog.getOpenFileName(self, "Buscar Archivo...", "C:\\", "Wanted Files (*.txt)(*.csv)")
        # src = cv2.imread(ruta, cv2.IMREAD_UNCHANGED) #Lee la ruta de la foto
        self.rutaArchivo = ruta
        #self.controladorDf = ManejoDF(self.rutaCSV)
        #Devuelve la excepción que hay en ManejoDF
        #self.mensaje = self.controladorDf.leerCSV(ruta)
        self.mostrarVentana3()
                    
    
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

    def mostrarAdvertencia(self):
        self.advertencia = Advertencia(self.mensaje)
        self.advertencia.show()
        
class Ventana3(QMainWindow):
    def __init__(self):
        super().__init__()
        self.widget = loadUi("diseno_ui\diseno_ventana3.ui", self)
        self.widget_size = self.widget.size()
        self.setWindowTitle('ventana 3')
        self.cerrar.clicked.connect(inicio.exit)
        self.min.clicked.connect(self.minimizar)
        self.frame.mouseMoveEvent = self.moveWindow
        self.BSiguiente.clicked.connect(self.mostrarVentana4)
    
    def minimizar(self):
        inicio.ventanaSubir.widget.showMinimized()

    def moveWindow(self, e):
        if e.buttons() == Qt.LeftButton:
            self.move(self.pos() + e.globalPos() - self.clickPosition)
            self.clickPosition = e.globalPos()
            e.accept()

    def mousePressEvent(self, event):
        self.clickPosition = event.globalPos()

    #def mostrarAdvertencia(self):
    #    self.advertencia = Advertencia(self.mensaje)
    #    self.advertencia.show()
    
    def mostrarVentana4(self):
        self.ventana4 = Ventana4()
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
    
    
class Ventana4(QMainWindow):
    def __init__(self):
        super().__init__()
        self.widget = loadUi("diseno_ui\diseno_ventana4.ui", self)
        self.widget_size = self.widget.size()
        self.setWindowTitle('ventana 4')
        self.cerrar.clicked.connect(inicio.exit)
        self.min.clicked.connect(self.minimizar)
        self.frame.mouseMoveEvent = self.moveWindow
        #self.BSiguiente.clicked.connect(self.mostrarVentana5)
        self.BAtras.clicked.connect(self.mostrarVentana3)
            
    
    def minimizar(self):
        inicio.ventanaSubir.ventana3.widget.showMinimized()

    def moveWindow(self, e):
        if e.buttons() == Qt.LeftButton:
            self.move(self.pos() + e.globalPos() - self.clickPosition)
            self.clickPosition = e.globalPos()
            e.accept()

    def mousePressEvent(self, event):
        self.clickPosition = event.globalPos()

    #def mostrarAdvertencia(self):
    #    self.advertencia = Advertencia(self.mensaje)
    #    self.advertencia.show()
    
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