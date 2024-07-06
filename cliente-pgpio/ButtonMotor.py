from lib.tkgpio import TkCircuit
from json import load

with open("ButtonMotor.json", "r") as file:
    configuration = load(file)

circuit = TkCircuit(configuration)
@circuit.run
def main():
    from time import sleep
    from lib.gpiozero import Motor, Button


    motor = Motor(backward=21, forward=22)
    switch = Button(11)


    while True:
        if switch.is_pressed:
            motor.backward(1)
        else:
            motor.backward(0)
        sleep(0.1)
