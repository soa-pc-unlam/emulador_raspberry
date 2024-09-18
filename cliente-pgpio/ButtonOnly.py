from lib.tkgpio.tkgpio import TkCircuit
from json import load

with open("ButtonOnly.json", "r") as file:
    configuration = load(file)

circuit = TkCircuit(configuration)
@circuit.run
def main():
    from time import sleep
    from lib.gpiozero import Button

    def button_pressed():
        print("Pressed")
    def button_released():
        print("Released")

    def button_pressed1():
        print("Pressed 1")

    def button_released1():
        print("Released 1")

    button = Button(8)
    button1 = Button(9)

    button.when_pressed = button_pressed
    button.when_released = button_released

    button1.when_pressed = button_pressed1
    button1.when_released = button_released1

    while True:
        sleep(0.1)
