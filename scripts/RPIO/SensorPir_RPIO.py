import RPi.GPIO as GPIO
import time
motionPin=12 #Conecto al pin 12 (GPIO 18)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(motionPin, GPIO.IN)
estado_anterior = False
estado_actual = False
time.sleep(4)

while True:
    motion=GPIO.input(motionPin)
    print(motion)
    if motion==1:
        print("********detecta")
    time.sleep(0.1)
