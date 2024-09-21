from time import sleep
from lib.gpiozero import Button
from lib.CreateCircuit import create_circuit

def main():

    def button_pressed():
        print("Pressed")
    def button_released():
        print("Released")

    def button_pressed1():
        print("Pressed 1")

    def button_released1():
        print("Released 1")

    button = Button(8, pull_up=False)
    button1 = Button(9, pull_up=False)

    button.when_pressed = button_pressed
    button.when_released = button_released

    button1.when_pressed = button_pressed1
    button1.when_released = button_released1

    while True:
        sleep(0.1)

create_circuit("ButtonOnly.json", main)