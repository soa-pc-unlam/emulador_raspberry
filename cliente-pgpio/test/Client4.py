from lib.tkgpio.tkgpio import TkCircuit
from json import load

with open("Client4.json", "r") as file:
    configuration = load(file)

circuit = TkCircuit(configuration)
@circuit.run
def main():
    from time import sleep
    from lib.gpiozero import LED, Button

    led = LED(21)
    button = Button(11)

    button.when_pressed = led.on
    button.when_released = led.off

    while True:
        sleep(0.1)