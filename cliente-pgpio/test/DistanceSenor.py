from lib.tkgpio.tkgpio import TkCircuit
from json import load

with open("DistanceSensor.json", "r") as file:
    configuration = load(file)

circuit = TkCircuit(configuration)
@circuit.run
def main():
    from time import sleep
    from lib.gpiozero import Button,DistanceSensor

    def button_pressed():
        print("Pressed")
    def button_released():
        print("Released")

    button = Button(11)
    distance_sensor = DistanceSensor(trigger=17, echo=18)
    button.when_pressed = button_pressed
    button.when_released = button_released

    while True:
        sleep(0.1)
