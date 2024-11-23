import speech_recognition as sr 
import noisereduce as nr
import librosa
import joblib
from joblib import dump, load
import numpy as np
import keyboard
import time
import pyaudio
import wave
from scipy.io import wavfile
import scipy.io
import pygame
import sys
import os
import subprocess

def grabacion():
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 2
    RATE = 16000
    RECORD_SECONDS = 5
    WAVE_OUTPUT_FILENAME = "grabacion2.wav"

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

modelo = joblib.load("Juego/modelo_entrenado85%.joblib",mmap_mode=None)

def prediceVector(audio):
    x,Fs = librosa.load('grabacion2.wav',mono = True, sr=16000) #import
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
    almacen = np.hstack((mfccs_sc, delta_mfcc_sc, delta2_mfccs_sc,melP))
    almacen = np.expand_dims(almacen, axis=0) #este epand_dims hay que cambiarlo y colocar lo del reshape que perefan hizo porque esta linea de codigo es de juan

    print(mfccs_sc.shape)
    mre= mfccs_sc.reshape(-1, mfccs_sc.shape[0])
    print(mre.shape)

    # Usa el modelo para predecir la clase de la nueva muestra
    predicted= modelo.predict(almacen)
    print("prueba",predicted )

    # Imprime la predicción de la clase
    etiquetas = ['abajo','arriba','cambiar','derecha','izquierda']
    #print(predicted_class[0])
    print(f'Se predijo la palabra: {etiquetas[predicted[0]]}')

    return predicted

terminar=False
while not terminar:
    grabacion()
    palabra=prediceVector("grabacion2.wav")
    print(palabra)

    if palabra == 0:
        keyboard.press('s')
        print('La tecla abajo ha sido pulsada!')
        time.sleep(0.1)
        keyboard.release('s')
    elif palabra == 1:
        keyboard.press('w')
        print('La tecla arriba ha sido pulsada!')
        time.sleep(0.1)
        keyboard.release('w')
    elif palabra == 2:
        keyboard.press('space')
        print('La tecla espacio ha sido pulsada!')
        time.sleep(0.1)
        keyboard.release('space')
    elif palabra == 3:
        keyboard.press('d')
        print('La tecla derecha ha sido pulsada!')
        time.sleep(0.1)
        keyboard.release('d')
    elif palabra == 4:
        keyboard.press('a')
        print('La tecla izquierda ha sido pulsada!')
        time.sleep(0.1)
        keyboard.release('a')
#------#

'''
def reconocedor():
   while True:
    
    try:
        reconocedor = sr.Recognizer()
        with sr.Microphone() as mic:
                print('Diga algo')
                reconocedor.adjust_for_ambient_noise(mic, duration=0.3)
                audio = reconocedor.listen(mic) 
                with open('Dijo.wav', 'wb') as dijo: 
                    dijo.write(audio.get_wav_data())
                    predice = prediceVector('Dijo.wav')
                    etiquetas = ['abajo','arriba','cambiar','derecha','izquierda']
                print(f'Se predijo la palabra: {etiquetas[predice[0]]}')
                    
                if 'abajo' in predice.lower():
                    teclaPresionada("s")
                
                elif 'arriba' in predice.lower():
                    teclaPresionada("w")
                    
                elif 'cambiar' in predice.lower():
                    teclaPresionada("space")
                    
                elif 'derecha' in predice.lower():
                    teclaPresionada("d")
                    
                elif 'izquierda' in predice.lower():
                    teclaPresionada("a")         
                
                
    except sr.unknownvalueerror():
                
        reconocedor = sr.Recognizer()
        continue


reconocedor = sr.Recognizer()
def reconocedor():
    try:
            with sr.Microphone() as mic:
                print('Diga algo')
                reconocedor.adjust_for_ambient_noise(mic, duration=0.3)
                audio = reconocedor.listen(mic) 
                with open('Dijo.wav', 'wb') as dijo: 
                    dijo.write(audio.get_wav_data())
                    predice = prediceVector('Dijo.wav')
                    etiquetas = ['abajo','arriba','cambiar','derecha','izquierda']
                print(f'Se predijo la palabra: {etiquetas[predice[0]]}')
                    
                if 'abajo' in predice.lower():
                    teclaPresionada("s")
                
                elif 'arriba' in predice.lower():
                    teclaPresionada("w")
                    
                elif 'cambiar' in predice.lower():
                    teclaPresionada("space")
                    
                elif 'derecha' in predice.lower():
                    teclaPresionada("d")
                    
                elif 'izquierda' in predice.lower():
                    teclaPresionada("a")         
                
                
    except:
        print("volviendo a escuchar... espere un momento")
        reconocedor()
        
    reconocedor()
reconocedor()


# inicializamos pygame
pygame.init()

# mostrar una ventana de 800 x 600
size = (900, 700)
screen = pygame.display.set_mode(size)

# colocamos un titulo de ventana
pygame.display.set_caption("BALL GAME")

# creamos variables
width, height = 900, 700
speed = [1, 1]
white = 255, 255, 255

# se crea un objeto ball a partir de una imagen y se obtiene su rectangulo
ballorg = pygame.image.load("Juego/images/ball.png.png")
ballrectorg = ballorg.get_rect()

# bola original
ball = ballorg
ballrect = ballrectorg

# imagen de cambio ball
ball2 = pygame.image.load("Juego/images/ball2.png.jpg")
ballrect2 = ball2.get_rect()

# se crea un objeto bate a partir de una imagen y se obtiene su rectangulo
bateorg = pygame.image.load("Juego/images/bate.png")
baterectorg = bateorg.get_rect()

bate = bateorg
baterect = baterectorg

# imagen de cambio bate
bate2 = pygame.image.load("Juego/images/bate2.png")
baterect2 = bate2.get_rect()

# poner en bate en el medio
baterect.move_ip(800, 260)

# variable para almacenar la posición de la pelota
posicion = ballrect.topleft

# creamos una variable para controlar el cambio de la imagen del bate
changing_bate = False

# posición inicial de la bola
ballrect.centerx = width // 2
ballrect.centery = height // 2

# iniciamos el bucle del jugo
run = True
while run:
    # eventos producidos en el juego
    # tiempo de 2 miliseg para que la bola vaya despacio
    pygame.time.delay(2)
    for event in pygame.event.get():
        # para salir de la ventana
        if event.type == pygame.QUIT:
            run = False
    # compruebo si se ha pulsado una tecla
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        baterect = baterect.move(0, -2)
    if keys[pygame.K_s]:
        baterect = baterect.move(0, 2)
    # dentro del bucle while, comprobamos si se ha presionado la barra espaciadora
    if keys[pygame.K_SPACE]:
        # solo cambiamos la imagen del bate una vez mientras se mantiene presionada la barra espaciadora
        if not changing_bate:
            if bate == bateorg:
                bate = bate2
            else:
                bate = bateorg
            changing_bate = True
    else:
        # si se suelta la barra espaciadora, permitimos que se cambie la imagen del bate de nuevo
        changing_bate = False

    # ver si hay colision
    if baterect.colliderect(ballrect) and baterect.collidepoint(ballrect.center):
        speed[0] = -speed[0]
    # movimiento de pelota
    ballrect = ballrect.move(speed)
    # comprobamos si la pelota llega a los limites de la ventana
    if ballrect.left < 0:
        # almacenar la posición actual de la pelota antes de cambiar la imagen
        posicion = ballrect.topleft
        if ball == ballorg:
            ball = ball2
        else:
            ball = ballorg
        # establecer la posición de la pelota a la posición anterior después de cambiar la imagen
        ballrect = ball.get_rect(topleft=posicion)
        # invertir la dirección de la pelota
        speed[0] = -speed[0]
    elif ballrect.right > width:
        speed[0] = -speed[0]
    if ballrect.top < 0 or ballrect.bottom > height:
        speed[1] = -speed[1]
    # pinto el fondo de blanco
    screen.fill(white)
    screen.blit(ball, ballrect)

    # Dibujo el bate
    screen.blit(bate, baterect)

    pygame.display.flip()

pygame.quit()
'''
