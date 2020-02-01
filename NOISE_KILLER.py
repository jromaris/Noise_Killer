import numpy as np
import numpy.matlib
from math import ceil

import matplotlib.pyplot as plt
import wave, struct, math, random

from scipy.io.wavfile import read
from scipy import *

import wavio 

from terminate_noise import terminate_noise

archivo="el_gato.wav"

#Tamaño de ventana
WINDOW_SIZE = 512*3

def read_audio(filename):
    wav = wavio.read(filename)
    input_audio=wav.data[:,0]
    input_audio = input_audio/np.max(np.abs(input_audio),axis=0)
    fs=wav.rate
    print("Frecuencia de muestreo",fs)
    return input_audio,fs

def cancel_noise(filename):

    #Leo el archivo de audio deseado
    input_audio, fs =read_audio(filename)

    #Vector que contiene la energía media del ruido 
    noise_mean=np.zeros(int(WINDOW_SIZE/2)+1)
    
    #Cantidad de ventanas 
    win_num=np.ceil(float(len(input_audio)-WINDOW_SIZE+1)/float(WINDOW_SIZE/2))
    
    #En caso de ser necesario agrego zero padding
    if (win_num*(WINDOW_SIZE/2)+WINDOW_SIZE/2) < len(input_audio):
        audio=zeros(len(input_audio))
    
    else:  
        audio=zeros(int(win_num*(WINDOW_SIZE/2)+WINDOW_SIZE/2))
    
    audio[0:len(input_audio)]=input_audio
    
    #Genero el vector de salida
    output=zeros(len(audio))
    
    #Genero la ventana de Hanning
    hanning=np.hanning(WINDOW_SIZE)
    
    #Media ventanta temporal utilizada para hacer Overlap and Add
    temp_win=zeros(int(WINDOW_SIZE/2))
    
    for i in range(int(win_num)):
    
        #Aplico la ventana
        curr_win=audio[int(WINDOW_SIZE/2)*i:int(WINDOW_SIZE/2)*(i+2)]*hanning
    
        #Opero
        curr_win,noise_mean=terminate_noise(curr_win,i,noise_mean,WINDOW_SIZE,10,8)
    
        #Calculo la salida
        output[i*int(WINDOW_SIZE/2):(i+1)*int(WINDOW_SIZE/2)]=curr_win[0:int(WINDOW_SIZE/2)]+temp_win
      
        #Actualizo la ventana temporal
        temp_win=curr_win[int(WINDOW_SIZE/2)-1:-1]
    
    freqs=np.linspace(0,fs*(WINDOW_SIZE/2-1)/WINDOW_SIZE,WINDOW_SIZE/2+1)
    
    #Grafico de la estimación espectral del ruido estacionario
    """
    print("Grafico amplitud de la estimación espectral del ruido")
    plt.plot(freqs,noise_mean**2)
    plt.xlabel("Frecuencia [Hz] ")
    plt.ylabel("Energía del ruido")
    plt.grid(True)
    plt.show()
    """

    """
    print("Grafico ambos audios con ruido y audio filtrado")
    #Grafico ambos audios con ruido y audio filtrado
    plt.figure(figsize=(15,10))
    plt.plot(audio,label="Audio con Ruido")
    plt.plot(output,label="Audio Filtrado")
    #plt.plot(original+2,label="Audio Sin Ruido")
    plt.grid(True)
    plt.legend(loc='lower left')
    plt.show()
    """

    #Escribo el wav del audio filtrado
    wavio.write("salida_filtrada.wav", output, fs, sampwidth=3) 
    return output, audio, fs


cancel_noise(archivo)

