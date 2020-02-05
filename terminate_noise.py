import numpy as np

#Attenuation constant
c = np.power(10,-3/2)

def terminate_noise(curr_win,win_number,noise_mean,window_len,noise_win_num,max_avrg_win):

    #Cantidad de ventanas iniciales en las que solo hay presente ruido
    NOISE_WINDOW_NUM = noise_win_num

    #Cantidad de ventanas de promediacion para la promediación en magnitud
    MAX_AVERAGING_WINDOW = max_avrg_win

    #Buffer Circular con las muestras para realizar la promediación en magnitud
    x_mean_buffer=np.zeros((int(window_len/2)+1,MAX_AVERAGING_WINDOW))

    noise_residual=np.zeros((int(window_len/2)+1,MAX_AVERAGING_WINDOW))

    #Aplico FFT a los datos
    data=np.fft.rfft(curr_win)
  
    #Valor absoluto de la FFT
    abs_data=np.absolute(data)
 
    #Agrego valor absoluto actual de lo muestreado al buffer circular de muestras previas
    x_mean_buffer[:,win_number%MAX_AVERAGING_WINDOW]=abs_data
 
    #Si solo hay ruido le tomo la media al módulo de la energía por banda espectral
    if win_number < NOISE_WINDOW_NUM:
 
        #Y calculo un promedio de energía por banda
        temp_mean=abs_data/(NOISE_WINDOW_NUM)
        #print(temp_mean)
        mean_noise=noise_mean+temp_mean
 
        noise_phase=np.angle(data)
 
        noise_residual=data- abs_data * np.exp(1j*noise_phase)
        out_data=data
 
    else:
        mean_noise=noise_mean
 
        #Obtengo el filtro estimador sin rectificación, teniendo en cuenta la promediación temporal del input
        H=1-noise_mean/np.mean(x_mean_buffer, axis=1)
 
        #Rectificación de Media Onda
        H=(H+np.absolute(H))/2
 
        #Aplico el filtro a los datos ventaneados
        out_data=data*H
 
        #Controlo la energia de la ventana en relación a la media del ruido
        energy_cntnt=20*np.log10(0.0001+np.sum(np.absolute(out_data/noise_mean)/len(out_data)))
        #print(energy_cntnt)
      
        if energy_cntnt < -15:
            out_data=data*c
 
    #Obtengo el audio ventaneado filtrado aplicando la ifft
    output=np.fft.irfft(out_data)
 
    return output,mean_noise 