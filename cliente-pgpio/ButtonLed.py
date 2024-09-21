from time import sleep
from lib.gpiozero import LED, Button
from lib.CreateCircuit import create_circuit


def main():
    def button_pressed():
        led.on()
    def button_released():
        led.off()

    led = LED(21)
    button = Button(11, pull_up=False)

    button.when_pressed = button_pressed
    button.when_released = button_released

    while True:
        sleep(0.1)

create_circuit("ButtonLed.json", main)