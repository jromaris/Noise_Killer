#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import os
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import*
from PyQt5.QtWidgets import QMessageBox
from PyQt5.uic import loadUi
from second_window import*

path = os.path.dirname(os.path.abspath(__file__))

class NK_gui(QMainWindow):
    
    def __init__(self):
        
        QMainWindow.__init__(self)

        loadUi(os.path.join(path, "noise_killer.ui"),self)
        

        self.audio_path= ""
        
        self.setWindowTitle("Noise killer")

        self.Button_seleccionar_audio.clicked.connect(self.buscar_audio)

        self.Button_kill_noise.clicked.connect(self.kill_noise)


    def buscar_audio(self):

        filePath, _ = QFileDialog.getOpenFileName(self,'Search file', '/home')
        

           
        self.Selected_audio.setText(str(filePath))
        self.audio_path =filePath
        print(self.audio_path)

    def kill_noise(self):
        if (self.audio_path != ""):
            #meter aca el noise_killer
            print("hace algo")
            self.open_window()
            #iniciar la nueva ventana
        else:
            self.popup_audio_not_selected()
            #self.open_window()

    def popup_audio_not_selected(self):
        msg = QMessageBox()
        msg.setWindowTitle("Select audio")
        msg.setText("Warning: no audio file selected")
        msg.setIcon(QMessageBox.Warning)
        x = msg.exec_()

    def open_window(self):
        self.window=Second_window(self.audio_path)
        self.window.setWindowTitle("Noise killer")
        self.window.show()



if __name__ == "__main__":
    app = QApplication([])
    window = NK_gui()
    window.show()
    app.exec_()








# Ui_MainWindow, QtBaseClass = uic.loadUiType( os.path.join(path, 'test.ui'))

# class MyApp(QtWidgets.QMainWindow, Ui_MainWindow):
#     def __init__(self):
#         QtWidgets.QMainWindow.__init__(self)
#         Ui_MainWindow.__init__(self)
#         self.setupUi(self)   #convierte a extension py lo de qt designer
        
#         #Aquí van los botones
#         self.Button_Import.clicked.connect(self.getCSV)
#         self.Button_Graph.clicked.connect(self.plot)
        


#     #Esta función abre el archivo CSV    
#     def getCSV(self):
#         filePath, _ = QtWidgets.QFileDialog.getOpenFileName(self, 'Open file', '/home')
#         if filePath != "":
#             print ("Dirección",filePath) #Opcional imprimir la dirección del archivo
#             self.df = pd.read_csv(str(filePath))
        


#     #Aquí van las nuevas funciones
#     def plot(self):
#         x=self.df['col1']
#         y=self.df['col2']
#         plt.plot(x,y)
#         plt.show()
#         estad_st="Estadisticas de col2: "+str(self.df['col2'].describe())
#         self.Result.setText(estad_st)

  
# if __name__ == "__main__":
#     app =  QtWidgets.QApplication(sys.argv)
#     window = MyApp()
#     window.show()