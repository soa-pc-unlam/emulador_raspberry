from gpiozero import Button, LED
from gpiozero.pins.pigpio import PiGPIOFactory
import os
import time

os.environ["PIGPIO_ADDR"] = "192.168.235.25"
os.environ["GPIOZERO_PIN_FACTORY"] = "pigpio"

button = Button(23)
led = LED(24)

led.source = button

while True:
   time.sleep(1)