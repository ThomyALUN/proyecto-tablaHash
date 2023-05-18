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
        self.ventanaSubir.setFixedSize(size)
        self.ventanaSubir.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.ventanaSubir.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.ventanaSubir.show()
        self.close()

class VentanaSubir(QMainWindow):
    def __init__(self):
        super().__init__()
        self.widget = loadUi("diseno_ui\diseno_subir.ui", self)
        self.setWindowTitle('Subir archivo')
        self.cerrar.clicked.connect(inicio.exit)
        self.min.clicked.connect(self.minimizar)
        self.frame.mouseMoveEvent = self.moveWindow
        self.BSubir.clicked.connect(self.seleccionarArchivo)    
        self.widget_size = self.widget.size()        

    def seleccionarArchivo(self):
        dirPath = os.getcwd()  # Directorio de la carpeta actual
        # Buscar archivo.csv
        ruta, _ = QFileDialog.getOpenFileName(self, "Buscar Archivo...", "C:\\", "Wanted Files (*.csv)")
        # src = cv2.imread(ruta, cv2.IMREAD_UNCHANGED) #Lee la ruta de la foto
        self.rutaCSV = ruta
        self.controladorDf = ManejoDF(self.rutaCSV)
        #Devuelve la excepción que hay en ManejoDF
        self.mensaje = self.controladorDf.leerCSV(ruta)
        if self.mensaje != None:
            self.mostrarAdvertencia()
            
        else:
           self.mostrarVentana2()
            
            
        print(self.rutaCSV)
        
    
    def minimizar(self):
        self.showMinimized()

    def moveWindow(self, e):
        if e.buttons() == Qt.LeftButton:
            self.move(self.pos() + e.globalPos() - self.clickPosition)
            self.clickPosition = e.globalPos()
            e.accept()

    def mousePressEvent(self, event):
        self.clickPosition = event.globalPos()

    def play(self):
        #posición del widget
        self.videoWidget.move(629,120)
        #self.videoWidget.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.player.play()
        self.videoWidget.show()   
        
    def mostrarVentana2(self):
        self.ventana2 = Ventana2(self.controladorDf)
        self.ventana2.raise_()
        self.ventana2.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.ventana2.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.ventana2.show()
        self.close() 
        self.player.stop()

    def mostrarAdvertencia(self):
        self.advertencia = Advertencia(self.mensaje)
        self.advertencia.show()
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