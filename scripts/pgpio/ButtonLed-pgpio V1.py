from gpiozero import Button, LED
from gpiozero.pins.pigpio import PiGPIOFactory
import os
from time import sleep

os.environ["PIGPIO_ADDR"] = "192.168.235.25"
os.environ["GPIOZERO_PIN_FACTORY"] = "pigpio"
def main():    
    
    def button_pressed():
        print("button pressed!")
        led2.toggle()
    
    led2 = LED(24)
    button = Button(23)
    button.when_pressed = button_pressed
    
    
    while True:
        sleep(0.1)

main()