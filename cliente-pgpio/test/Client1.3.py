import os
from lib.gpiozero import MotionSensor
from time import sleep
from lib.gpiozero.pins.pigpio import PiGPIOFactory

factory = PiGPIOFactory(host='127.0.0.1', port=5000)
def motion_detected():
    print("Motion Detected")
def motion_no_detected():
    print("Motion No Detected")

#Sensores
motion_sensor = MotionSensor(pin=25,pin_factory=factory)

#Handlers
motion_sensor.when_motion = motion_detected
motion_sensor.when_no_motion = motion_no_detected

while True:
    sleep(0.1)
