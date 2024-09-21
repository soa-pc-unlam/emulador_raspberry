from time import sleep
from lib.gpiozero import Motor, Button
from lib.CreateCircuit import create_circuit
def main():

    speed= 0
    motor = Motor(backward=21, forward=22)
    switchSpeed= Button(11, pull_up=False)
    btnReversePolarity = Button(12, pull_up=False)


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


create_circuit("ButtonMotor.json", main)