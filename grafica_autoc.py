from cmath import log10
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import soundfile as sf

audio = "pitch_db/train/rl002.wav"
#Usaremos el fichero prueba.wav para las diferentes gráficas
read_wave, fm = sf.read(audio) 
#Leemos el fichero
read_wave_auto=read_wave[int(fm*0.33):int(fm*0.33+fm*0.03)] 
#Cortamos la señal de entrada a un punto donde parece ser muy sonora y con una duración de 30 ms
time = (np.linspace(start=0, stop = (len(read_wave_auto)-1), num = len(read_wave_auto)))/fm 
#Calculamos el vector de tiempo para las gráficas

#Calculamos la autocorrelación de la señal recortada
autocorrelacio = np.correlate(read_wave_auto, read_wave_auto, "full")
autocorrelacio = autocorrelacio/autocorrelacio[int(len(autocorrelacio)/2)]
autocorrelacio = autocorrelacio[int(len(autocorrelacio)/2):]

#Creamos el vector espacial para representar la autocorrelación
xautocorrelacio = np.arange(len(autocorrelacio))

#Subplot1 con la amplitud de la señal.
plt.subplot(2,1,1)
plt.title("Señal temporal")
plt.ylabel("Amplitud")
plt.plot(time,read_wave_auto)
#Subplot2 con la autocorrelación de la señal.
plt.subplot(2,1,2)
plt.title("Autocorrelación de la señal de voz")
plt.xlabel("Muestras")
plt.ylabel("Autocorrelación")
plt.plot(xautocorrelacio, autocorrelacio)
plt.show()


##Gráficas de la potencia, rx[1]/rx[0], rx[lag]/rx[0]
pot=[]
rxx1=[]
rxxlag=[]
#Abrimos, leemos y cerramos el fichero con los datos guardados.
f=open("ficheropotrxx01.txt","r")
info=f.read()
f.close()
#Separamos la información por filas
filas=info.split("\n")
for i in filas:
    #Separamos las filas para guardar cada variable en su vector
    temp=i.split("\t")
    pot.append(float(temp[0]))
    rxx1.append(float(temp[1]))
    rxxlag.append(float(temp[2]))
numtramas=range(len(filas))

#Subplot de la potencia
plt.subplot(3,1,1)
plt.title("Potencia")
plt.xlabel("Tramas")
plt.ylabel("Potencia [dB]")
plt.plot(numtramas,pot)
#Subplot de Rx[1]/Rx[0]
plt.subplot(3,1,2)
plt.title("Rx[1]/Rx[0]")
plt.xlabel("Tramas")
plt.plot(numtramas,rxx1)
#Subplot de Rx[Lag]/Rx[0]
plt.subplot(3,1,3)
plt.title("Rx[Lag]/Rx[0]")
plt.xlabel("Tramas")
plt.plot(numtramas,rxxlag)
plt.show()


##Central clipping
#Creamos el vector temporal de toda la señal.
temps = (np.linspace(start=0, stop = (len(read_wave)-1), num = len(read_wave)))/fm 
#Definimos el umbral del clipping, este ha sido escogido para una buena visualización del efecto que tiene
umbral=0.06
#Creamos una lista con los datos de la señal para una fácil manipulación
wave_clip=list(read_wave)
for i in range(len(read_wave)-1):
    #Si la señal en valor absoluto se encuentra por debajo del umbral, la ponemos a cero.
    if -umbral<wave_clip[i]<umbral:
        wave_clip[i]=0
#Subplot para la señal original
plt.subplot(2,1,1)
plt.title("Señal original")
plt.ylabel("Amplitud")
plt.plot(temps, read_wave)
#Subplot para la señal procesada con el central clipping a 0.6
plt.subplot(2,1,2)
plt.title("Señal con el central clipping")
plt.xlabel("Tiempo (s)")
plt.ylabel("Amplitud")
plt.plot(temps, wave_clip)
plt.show()


##Mediana
#Creamos un vector de f0 para trabajar.
f0=[25,50,50,50,100,100,150,100,75,100,100,150,150,150,100,100,125,150,125,100,100,100,50,75,50,75,100,100,120]
f0_mediana=[]
#Añadimos la primera muestra
f0_mediana.append(f0[0])
#Para todo el vector, miramos cual es el valor mediano entre la muestra actual, la anterior y la posterior
#Será la mediana (central en orden creciente/decreciente) la que guardaremos en el vector procesado.
for i in range(1,len(f0)-1):
    if f0[i-1]<=f0[i]<=f0[i+1] or f0[i+1]<=f0[i]<=f0[i-1]:
        f0_mediana.append(f0[i])
    elif f0[i]<=f0[i-1]<=f0[i+1] or f0[i+1]<=f0[i-1]<=f0[i]:
        f0_mediana.append(f0[i-1])
    elif f0[i-1]<f0[i+1]<=f0[i] or f0[i]<=f0[i+1]<f0[i-1]:
        f0_mediana.append(f0[i+1])
#Añadimos la última muestra
f0_mediana.append(f0[len(f0)-1])
#Subplot con la señal original
plt.subplot(2,1,1)
plt.title("Señal original")
plt.ylabel("F0")
plt.plot(range(len(f0)),f0)
#Subplot con la señal procesada
plt.subplot(2,1,2)
plt.title("Con filtro mediana")
plt.xlabel("Tramas")
plt.ylabel("F0")
plt.plot(range(len(f0_mediana)),f0_mediana)
plt.show()