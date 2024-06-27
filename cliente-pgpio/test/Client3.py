from tkgpio import TkCircuit
from json import load
import os

with open("Client3.json", "r") as file:
    configuration = load(file)

os.environ["PIGPIO_ADDR"] = "127.0.0.1"
os.environ["PIGPIO_PORT"] = "5000"
os.environ["GPIOZERO_PIN_FACTORY"] = "pigpio"

circuit = TkCircuit(configuration)
@circuit.run
def main():
    from time import sleep
    from gpiozero import LED, Button

    def button_pressed():
        print("Button pressed")
    def button_released():
        print("Button released")
    button = Button(11)

    button.when_pressed = button_pressed
    button.when_released = button_released

    while True:
        sleep(0.1)