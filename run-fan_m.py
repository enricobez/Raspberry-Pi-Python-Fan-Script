#!/usr/bin/env python3
# Author: Enrico Bez <zeben91@gmail.com>
 
import os
from time import sleep
import signal
import sys
import RPi.GPIO as GPIO
import datetime

pin = 14 # The pin ID, edit here to change it
maxTMP = 70 # The maximum temperature in Celsius after which we trigger the fan
superTMP = 77
def setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pin, GPIO.OUT)
    GPIO.setwarnings(False)
    loggingACC()
    return()

def getCPUtemperature():
    res = os.popen('vcgencmd measure_temp').readline()
    temp =(res.replace("temp=","").replace("'C\n",""))
    deg = u'\xb0'  # utf code for degree
    deg = deg.encode('utf8')
    print("temp is {0}".format(temp) + deg) #Uncomment here for testing 
    return temp
def loggingACC():
    now=datetime.datetime.now()
    with open("/home/pi/Development/fan.log", mode='a') as file:
        deg = u'\xb0'  # utf code for degree
        deg = deg.encode('utf8')
        file.write('------------------ SISTEMA AVVIATO ------------------\n%s: Temperatura = %s%s\n' %(now.strftime("%d-%m-%Y %H:%M:%S"),getCPUtemperature(),deg))
        file.close()
def loggingON():
    now=datetime.datetime.now()
    with open("/home/pi/Development/fan.log", mode='a') as file:
        deg = u'\xb0'  # utf code for degree
        deg = deg.encode('utf8')
        file.write('%s: Temperatura = %s%s Ventola ON\n' %(now.strftime("%d-%m-%Y %H:%M:%S"),getCPUtemperature(),deg))
        file.close()
def loggingOFF():
    now=datetime.datetime.now()
    with open("/home/pi/Development/fan.log", mode='a') as file:
        deg = u'\xb0'  # utf code for degree
        deg = deg.encode('utf8')
        file.write('%s: Temperatura = %s%s Ventola OFF\n' %(now.strftime("%d-%m-%Y %H:%M:%S"),getCPUtemperature(),deg))
        file.close()
def loggingSUPER():
    now=datetime.datetime.now()
    with open("/home/pi/Development/fan.log", mode='a') as file:
        deg = u'\xb0'  # utf code for degree
        deg = deg.encode('utf8')
        file.write('%s: Temperatura = %s%s Ventola ON (SUPER MODE)\n' %(now.strftime("%d-%m-%Y %H:%M:%S"),getCPUtemperature(),deg))
        file.close()
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
def getTEMP():
    CPU_temp = float(getCPUtemperature())
    if CPU_temp>maxTMP and CPU_temp<superTMP:
        fanON()
    elif CPU_temp>superTMP:
	    fanSUPER()
    else:
        fanOFF()
    return()
def setPin(mode): # A little redundant function but useful if you want to add logging
    GPIO.output(pin, mode)
    return()

try:
    setup() 
    while True:
        getTEMP()
        sleep(5) # Read the temperature every 5 sec, increase or decrease this limit if you want
except KeyboardInterrupt: # trap a CTRL+C keyboard interrupt 
    GPIO.cleanup() # resets all GPIO ports used by this program


