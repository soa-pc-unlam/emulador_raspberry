import os
from lib.gpiozero import Button
from time import sleep

from lib.gpiozero.pins.pigpio import PiGPIOFactory

# os.environ["PIGPIO_ADDR"] = "127.0.0.1"
# os.environ["PIGPIO_PORT"] = "5000"
# os.environ["GPIOZERO_PIN_FACTORY"] = "pigpio"

factory = PiGPIOFactory(host='127.0.0.1', port=5000)

def button_pressed():
    print("Button Pressed")

def button_released():
    print("Button Released")

button = Button(11,hold_repeat=False, pin_factory=factory)
button.when_pressed = button_pressed
button.when_released = button_released

while True:
    sleep(1)
