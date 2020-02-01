from adafilt import FastBlockLMSFilter
from adafilt.io import FakeInterface
import wavio
import matplotlib.pyplot as plt
import numpy as np

def read_audio(filename):
    wav = wavio.read(filename)
    input_audio=wav.data[:,0]
    input_audio = input_audio/np.max(np.abs(input_audio),axis=0)
    fs=wav.rate
    print("Frecuencia de muestreo",fs)
    return input_audio,fs

def adaptive_cancel(audio_file,noise_file,M):

	length = M  # number of adaptive FIR filter taps
	blocklength = M  # length of I/O buffer and blocksize of filter
	
	audio_signal,fs =read_audio(audio_file)
	
	noise_signal,fs =read_audio(noise_file)
	
	number_of_blocks =  len(audio_signal)//M
	
	error = np.zeros(number_of_blocks*M)
	
	padd_audio = audio_signal[:number_of_blocks*M]
	padd_noise = noise_signal[:number_of_blocks*M]
	audio_blocks = np.array_split(padd_audio,number_of_blocks)
	noise_blocks = np.array_split(padd_noise,number_of_blocks)
	
	filt = FastBlockLMSFilter(length, blocklength, stepsize=0.1, leakage=0.9999, constrained=False, normalized=True)
	
	elog = []
	felog = []
	wslog = []
	ylog = []
	dlog = []
	
	for i in range(number_of_blocks):
	
	    # filter prediction
	    y = filt.filt(noise_blocks[i])
	
	    # error signal
	    e = y - audio_blocks[i]
	    filt.adapt(noise_blocks[i], e)
	
	    elog.append(e)
	    dlog.append(audio_blocks[i])
	    ylog.append(y)
	    wslog.append(filt.w)
	
	y_out=np.concatenate(ylog)
	d_out=np.concatenate(dlog)
	e_out=np.concatenate(elog)
	plt.plot(padd_noise,label="Signal_with_noise")
	plt.plot(y_out,label="Noise_Estimation")
	plt.plot(e_out,label="Output")
	#plt.plot(new_auxd+1.5,label="Deseada con offset")
	plt.legend(loc='lower left')
	plt.grid(True)
	plt.xlabel('Sample number')
	plt.ylabel('Amplitude')
	plt.show()
	
	plt.title("Filter Coefficient")
	plt.plot(np.array(wslog))
	plt.xlabel("Block Number")
	plt.ylabel("Coefficient Magnitude")
	plt.grid(True)
	plt.show()
	
	wavio.write("salida_filtrada_LMS.wav", e_out, fs, sampwidth=3) 

	return e_out

adaptive_cancel("los_sinso_con_ruido_nuevo.wav","ruido.wav",100)
