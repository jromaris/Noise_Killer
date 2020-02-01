import sys
import os
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import*
from PyQt5.QtWidgets import QMessageBox
from PyQt5.uic import loadUi
import NOISE_KILLER as NK
import sounddevice as sd
import Adaptive_filter as adf

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
        
        self.nk_audio, self.original_audio, self.fs = NK.cancel_noise(self.audio_path) 

        self.original_audio, self.af_audio, self.fs, _ = adf.adaptive_cancel(self.audio_path,self.noise_path,100)    

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
            self.MplWidget.canvas.axes.clear()
            if (chk_o):
                self.MplWidget.canvas.axes.plot(self.original_audio,label="Audio con ruido")
                print("press original")
            if chk_nk:
                self.MplWidget.canvas.axes.plot(self.nk_audio,label="Audio filtrado")
                print("grahp nk")
            if chk_af:
                self.MplWidget.canvas.axes.plot(self.af_audio,label="Audio filtrado adaptativamente")
                print("graph af")
            self.MplWidget.canvas.axes.grid(True)
            self.MplWidget.canvas.axes.legend(loc='lower left')
            self.MplWidget.canvas.draw()

            
    def play_original(self):
        print("play original")
        sd.play(self.original_audio,self.fs)
        

    def play_NK(self):
        print("play NK")
        sd.play(self.nk_audio,self.fs) 
        

    def play_AF(self):
        sd.play(self.af_audio,self.fs) 
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