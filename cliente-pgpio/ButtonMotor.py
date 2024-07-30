from lib.tkgpio import TkCircuit
from json import load

with open("ButtonMotor.json", "r") as file:
    configuration = load(file)

circuit = TkCircuit(configuration)
@circuit.run
def main():
    from time import sleep
    from lib.gpiozero import Motor, Button

    speed= 0
    motor = Motor(backward=21, forward=22)
    switchSpeed= Button(11)
    btnReversePolarity = Button(12)


    while True:

        if switchSpeed.is_pressed:
            speed=1
        else:
            speed=0.1

        if btnReversePolarity.is_pressed:
            motor.forward(speed)
        else:
            motor.backward(speed)
        sleep(0.1)
