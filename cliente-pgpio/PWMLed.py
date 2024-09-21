from lib.gpiozero import PWMLED
from time import sleep
from lib.gpiozero import Button
from lib.CreateCircuit import create_circuit


def main():

    led = PWMLED(21)
    switchLighting= Button(11)
    btnOffLed = Button(12, pull_up=False)

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

create_circuit("PWMLed.json", main)