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

autocorrelacio = np.correlate(read_wave_auto, read_wave_auto, "full")
autocorrelacio = autocorrelacio/autocorrelacio[int(len(autocorrelacio)/2)]
#ens quedem només amb la primera meitat 
autocorrelacio = autocorrelacio[int(len(autocorrelacio)/2):]

#generem el eix x que sigui igual de llarg que la longitud de l'autocorrelació en mostres
xautocorrelacio = np.arange(len(autocorrelacio))
#plt.xscale("log")
#fem la gràfica de la senyal sola
plt.subplot(2,1,1)
plt.title("Señal temporal")
plt.ylabel("Amplitud")
plt.plot(time,read_wave_auto)

#fem la gràfica de l'autocorrelació
plt.subplot(2,1,2)
plt.title("Autocorrelación de la señal de voz")
plt.xlabel("Muestras")
plt.ylabel("Autocorrelación")
plt.plot(xautocorrelacio, autocorrelacio)
#Ho mostrem
plt.show()
rxx0=[]
rxx1=[]
rxxmax=[]
#for i in range(0,len(read_wave)-1,int(fm*0.015)):
#    read_wave_auto=read_wave[int(fm*i):int(fm*i+fm*0.03)]
#    rxx = np.correlate(read_wave_auto, read_wave_auto, "same")
#    rxx = rxx/rxx[int(len(rxx)/2)]
#    rxx0.append(rxx[0])
#    rxx1.append(rxx[1]/rxx[0])
#    rxxmax.append((np.max(rxx)-rxx[0])/rxx[0])
#    ntramas=i

#plt.subplot(3,1,1)
#plt.title("Senyal temporal")
#plt.xlabel("Temps (s)")
#plt.ylabel("Amplitud")
#plt.plot(i,rxx0)

#fem la gràfica de l'autocorrelació
#plt.subplot(3,1,3)
#plt.title("Autocorrelació de la senyal de veu")
#plt.xlabel("Mostres")
#plt.ylabel("Autocorrelació")
#plt.plot(i,rxx1)
#plt.subplot(3,1,3)
#plt.title("Autocorrelació de la senyal de veu")
#plt.xlabel("Mostres")
#plt.ylabel("Autocorrelació")
#plt.plot(i,rxxmax)
#Ho mostrem
#plt.show()


##Central clipping
temps = (np.linspace(start=0, stop = (len(read_wave)-1), num = len(read_wave)))/fm 
coef1=0.060
umbral=coef1*1
wave_clip=list(read_wave)
for i in range(len(read_wave)-1):
    if -umbral<wave_clip[i]<umbral:
        wave_clip[i]=0
plt.subplot(2,1,1)
plt.title("Señal original")
plt.ylabel("Amplitud")
plt.plot(temps, read_wave)

#fem la gràfica de l'autocorrelació
plt.subplot(2,1,2)
plt.title("Señal con el central clipping")
plt.xlabel("Tiempo (s)")
plt.ylabel("Amplitud")
plt.plot(temps, wave_clip)
#Ho mostrem
plt.show()


##Mediana

f0=[25,50,50,50,100,100,150,100,75,100,100,150,150,150,100,100,125,150,125,100,100,100,50,75,50,75,100,100,120]
f0_mediana=[]
f0_mediana.append(f0[0])
print(f0_mediana)
for i in range(1,len(f0)-2):
    if f0[i-1]<=f0[i]<=f0[i+1] or f0[i+1]<=f0[i]<=f0[i-1]:
        f0_mediana.append(f0[i])
    elif f0[i]<=f0[i-1]<=f0[i+1] or f0[i+1]<=f0[i-1]<=f0[i]:
        f0_mediana.append(f0[i-1])
    elif f0[i-1]<f0[i+1]<=f0[i] or f0[i]<=f0[i+1]<f0[i-1]:
        f0_mediana.append(f0[i+1])
f0_mediana.append(f0[len(f0)-2])
f0_mediana.append(f0[len(f0)-1])
plt.subplot(2,1,1)
plt.title("Señal original")
plt.ylabel("F0")
plt.plot(range(len(f0)),f0)
plt.subplot(2,1,2)
plt.title("Con filtro mediana")
plt.xlabel("Tramas")
plt.ylabel("F0")
plt.plot(range(len(f0_mediana)),f0_mediana)
plt.show()