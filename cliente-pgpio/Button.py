from math import trunc

from lib.CreateCircuit import create_circuit
from time import sleep
from lib.gpiozero import Button


'''definicion de funciones'''
def button_pressed():
    print("Pressed")

def button_released():
    print("Released")


def main():

    button = Button(11, pull_up=False)

    button.when_pressed = button_pressed
    button.when_released = button_released

    while True:
        sleep(0.1)


create_circuit("Button.json", main)