import sys
import os
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import*
from PyQt5.QtWidgets import QMessageBox
from PyQt5.uic import loadUi


path = os.path.dirname(os.path.abspath(__file__))

class Second_window(QWidget):

    def __init__(self,audio_name,noise_name = None,parent = None):

        QWidget.__init__(self, parent)
        
        loadUi(os.path.join(path, "second_window.ui"),self)
        #self.ui = Ui.Form()
        self.Button_graph.clicked.connect(lambda: self.update_graph(self.check_original.isChecked(),self.check_nk.isChecked(),self.check_af.isChecked()))
        self.Button_clear.clicked.connect(self.clear_graph)
        self.Button_playO.clicked.connect(self.play_original)
        self.Button_playNK.clicked.connect(self.play_NK)
        self.Button_playAF.clicked.connect(self.play_AF)
        self.audio_path= audio_name
        self.noise_path= noise_name
        print(self.audio_path)
        

    def clear_graph(self):
        print("borrar todos los datos")
        
        
    def update_graph(self,chk_o,chk_nk,chk_af):
        if(self.check_freq.isChecked() and self.check_time.isChecked()):
            self.popup_not_posible()
        elif not(self.check_freq.isChecked()) and not(self.check_time.isChecked()):
            self.popup_not_posible2()
            
        else:
            if(self.check_freq.isChecked()):
                aux=0       #para saber si hacer el espectograma o en tiempo
            elif self.check_time.isChecked():
                aux=1
            if (chk_o):
                print("press original")
            if chk_nk:
                print("grahp nk")
            if chk_af:
                print("graph af")

            
    def play_original(self):
        print("play original")
    

    def play_NK(self):
        print("play NK")

    def play_AF(self):
        print("play AF")





    def popup_not_posible(self):
        msg = QMessageBox()
        msg.setWindowTitle("Fatal Error")
        msg.setText("Please select time or frequency not BOTH")
        msg.setIcon(QMessageBox.Critical)
        x = msg.exec_()

    def popup_not_posible2(self):
        msg = QMessageBox()
        msg.setWindowTitle("Fatal Error")
        msg.setText("Please select one option: time or frequency")
        msg.setIcon(QMessageBox.Critical)
        x = msg.exec_()