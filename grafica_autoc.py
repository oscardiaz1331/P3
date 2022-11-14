from cmath import log10
#import matplotlib.pyplot as plt
import soundfile as sf
import numpy as np

from wave import WAVE_FORMAT_PCM
import wave
##import statsmodels.api as sm
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np

#audio = "pureba.wav"
#llegim el fitxer de veu de prueba.wav
prueba, fs = sf.read("Nova-gravació-6.wav")
#diem el temps
prueba=prueba[32000:32000*2]
time_sf = (np.linspace(start=0, stop = (len(prueba)-1), num = len(prueba)))/fs
#calculem l'autocorrelació amb la funció que ens don la llibreria numpy
autocorrelacio = np.correlate(prueba, prueba, "full")
autocorrelacio = autocorrelacio/autocorrelacio[int(len(autocorrelacio)/2)]
#ens quedem només amb la primera meitat 
autocorrelacio = autocorrelacio[int(len(autocorrelacio)/2):]

#generem el eix x que sigui igual de llarg que la longitud de l'autocorrelació en mostres
xautocorrelacio = np.arange(len(autocorrelacio))
#plt.xscale("log")
#fem la gràfica de la senyal sola
plt.subplot(2,1,1)
plt.title("Senyal temporal")
plt.xlabel("Temps (s)")
plt.ylabel("Amplitud")
plt.plot(time_sf, prueba)

#fem la gràfica de l'autocorrelació
plt.subplot(2,1,2)
plt.title("Autocorrelació de la senyal de veu")
plt.xlabel("Mostres")
plt.ylabel("Autocorrelació")
plt.plot(xautocorrelacio, autocorrelacio)
#Ho mostrem
plt.show()
