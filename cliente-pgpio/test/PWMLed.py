from lib.gpiozero import PWMLED
from lib.tkgpio import TkCircuit
from json import load

with open("PWMLed.json", "r") as file:
    configuration = load(file)

circuit = TkCircuit(configuration)
@circuit.run
def main():
    from time import sleep
    from lib.gpiozero import Button

    led = PWMLED(21)
    switchLighting= Button(11)
    btnOffLed = Button(12)

    ligthing =0

    while True:

        if btnOffLed.is_pressed:
            ligthing=0
        else:
            if switchLighting.is_pressed:
                ligthing=1
            else:
                ligthing=0.5

        led.value=ligthing

        sleep(0.1)
