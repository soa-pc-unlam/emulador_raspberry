from gpiozero import Servo
from time import sleep
import os

os.environ["GPIOZERO_PIN_FACTORY"] = "pigpio"
os.environ["PIGPIO_ADDR"] = "192.168.30.12"

myGPIO = 18

servo = Servo(myGPIO)
print("Rassberry Pi Servo")
while True:
    servo.min()
    print("min")
    sleep(1)
    servo.mid()
    print("mid")
    sleep(1)
    servo.max()
    print("max")
    sleep(1)
