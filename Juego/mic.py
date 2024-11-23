import pyaudio
import wave
import librosa
import numpy as np
import joblib
from joblib import dump
import noisereduce as nr


CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
RECORD_SECONDS = 5
WAVE_OUTPUT_FILENAME = "grabacion.wav"

p = pyaudio.PyAudio()

stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)

print("Grabando...")

frames = []

for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    data = stream.read(CHUNK)
    frames.append(data)

print("Grabación finalizada.")

stream.stop_stream()
stream.close()
p.terminate()

wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
wf.setnchannels(CHANNELS)
wf.setsampwidth(p.get_sample_size(FORMAT))
wf.setframerate(RATE)
wf.writeframes(b''.join(frames))
wf.close()

modelo = joblib.load('modelo_entrenado85%.joblib',mmap_mode=None)

x,Fs = librosa.load('grabacion.wav',mono = True, sr=16000) #import
audio_trim = librosa.effects.trim(x, top_db=20) # recorte silencios
normalized_audio = librosa.util.normalize(audio_trim[0])   #normalizacion       
audio_noise_reduce = nr.reduce_noise(normalized_audio, sr=Fs) #reduccion ruido
S = librosa.feature.melspectrogram(y=audio_noise_reduce,sr=Fs, n_mels=40, n_fft=2048,hop_length=512) #espectograma de mel, espectro de potencia stft transformada de fourier corta , el hoplenght es donde se solapan, donde se cruzan y n_fft es cantidad de muestras de la transformada de fourier
melP= np.mean(S.T, axis=0)         
mfccs = librosa.feature.mfcc(y=np.float32( audio_noise_reduce),sr=Fs, n_fft=512, hop_length=256, n_mfcc=13)
mfccs_sc = np.mean(mfccs.T, axis=0) #Esta línea calcula la media de los MFCC calculados en la línea anterior
delta_mfcc=librosa.feature.delta( mfccs) #derivada, representa cambios de tonalidad
delta_mfcc_sc = np.mean(delta_mfcc.T, axis=0)
delta2_mfcc=librosa.feature.delta(mfccs, order=2)# segunda derivada // CUANDO SE VAN A SACAR LAS DELTAS SE ESTA ENVIANDO EL MFCC, ESE SE DEBE ENVIAR O ES EL DELTA_MFCC
delta2_mfccs_sc = np.mean(delta2_mfcc.T, axis=0)
mfccs_sc = np.hstack((mfccs_sc, delta_mfcc_sc, delta2_mfccs_sc,melP))

print(mfccs_sc.shape)
mre= mfccs_sc.reshape(-1, mfccs_sc.shape[0])
print(mre.shape)

# Usa el modelo para predecir la clase de la nueva muestra
predicted= modelo.predict(mre)
print(predicted)

# Imprime la predicción de la clase
etiquetas = ['abajo','arriba','cambiar','derecha','izquierda']
#print(predicted_class[0])
print(f'Se predijo la palabra: {etiquetas[predicted[0]]}')