#!/usr/bin/env python3
# Author: Enrico Bez <email@enricobez.it>
import os
from time import sleep
import signal
import sys
import RPi.GPIO as GPIO
import datetime
pin = 14 # Identificativo del pin
maxTMP = 70 # La temperatura massima in gradi Celsius oltre la quale si attiva la ventola
superTMP = 77 # La temperatura estrema in gradi Celsius oltre la quale si attiva la ventola per più tempo
# Funzione per il setup delle porte GPIO
def setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pin, GPIO.OUT)
    GPIO.setwarnings(False)
    loggingACC() # Funzione per logging all'accensione del Raspberry
    return()
# Funzione per ottenere il valore delle temperatura si sistema della CPU
def getCPUtemperature():
    res = os.popen('vcgencmd measure_temp').readline()
    temp =(res.replace("temp=","").replace("'C\n",""))
    deg = u'\xb0'  # utf code for degree
    deg = deg.encode('utf8')
    # print("temp is {0}".format(temp) + deg) # Scommenta per test 
    return temp
# Funzione per logging all'accensione del Raspberry
def loggingACC():
    now=datetime.datetime.now()
    with open("/home/pi/Development/RunFan/fan.log", mode='a') as file:
        deg = u'\xb0'  # utf code for degree
        deg = deg.encode('utf8')
        file.write('------------------ SISTEMA AVVIATO ------------------\n%s: Temperatura = %s%s\n' %(now.strftime("%d-%m-%Y %H:%M:%S"),getCPUtemperature(),deg))
        file.close()
# Funzione per logging all'accensione della ventola
def loggingON():
    now=datetime.datetime.now()
    with open("/home/pi/Development/RunFan/fan.log", mode='a') as file:
        deg = u'\xb0'  # utf code for degree
        deg = deg.encode('utf8')
        file.write('%s: Temperatura = %s%s Ventola ON\n' %(now.strftime("%d-%m-%Y %H:%M:%S"),getCPUtemperature(),deg))
        file.close()
# Funzione per logging allo spegnimento della ventola
def loggingOFF():
    now=datetime.datetime.now()
    with open("/home/pi/Development/RunFan/fan.log", mode='a') as file:
        deg = u'\xb0'  # utf code for degree
        deg = deg.encode('utf8')
        file.write('%s: Temperatura = %s%s Ventola OFF\n' %(now.strftime("%d-%m-%Y %H:%M:%S"),getCPUtemperature(),deg))
        file.close()
# Funzione per logging all'accensione della ventola nel caso di temperature molto alte
def loggingSUPER():
    now=datetime.datetime.now()
    with open("/home/pi/Development/fan.log", mode='a') as file:
        deg = u'\xb0'  # utf code for degree
        deg = deg.encode('utf8')
        file.write('%s: Temperatura = %s%s Ventola ON (SUPER MODE)\n' %(now.strftime("%d-%m-%Y %H:%M:%S"),getCPUtemperature(),deg))
        file.close()
# Funzioni per la gestione della ventola
def fanON():
    setPin(True)
    loggingON()
    sleep(90) # La ventola va per 90 secondi
    loggingOFF()
    return()
def fanSUPER():
    setPin(True)
    loggingSUPER()
    sleep(150) # La ventola va per 150 secondi
    loggingOFF()
    return()
def fanOFF():
    setPin(False)
    sleep(10) # La ventola si spegne per 10 secondi
    return()
# Algoritmo si esecuzione principale da cui richiamo le varie funzioni
def getTEMP():
    CPU_temp = float(getCPUtemperature())
    if CPU_temp>maxTMP and CPU_temp<superTMP:
        fanON()
    elif CPU_temp>superTMP:
        fanSUPER()
    else:
        fanOFF()
    return()
def setPin(mode): # Una funzione un po' ridondante ma utile se si vuole aggiungere il logging
    GPIO.output(pin, mode)
    return()
    
try:
    setup() 
    while True:
        getTEMP()
        sleep(5) # Leggere la temperatura ogni 5 sec, aumentare o diminuire questo limite se si desidera
except KeyboardInterrupt: # Serve per intrappolare l'interrupt da tastiera CTRL+C 
    GPIO.cleanup() # resetta tutte le porte GPIO utilizzate da questo programma


