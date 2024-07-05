from lib.tkgpio import TkCircuit
from json import load

with open("ButtonLed.json", "r") as file:
    configuration = load(file)

circuit = TkCircuit(configuration)
@circuit.run
def main():
    from time import sleep
    from lib.gpiozero import LED, Button

    def button_pressed():
        led.on()
    def button_released():
        led.off()

    led = LED(21)
    button = Button(11)

    button.when_pressed = button_pressed
    button.when_released = button_released

    while True:
        sleep(0.1)
