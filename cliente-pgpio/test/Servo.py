from lib.gpiozero import Servo,Button
from lib.tkgpio import TkCircuit
from json import load
from time import sleep


with open("Servo.json", "r") as file:
    configuration = load(file)

circuit = TkCircuit(configuration)
@circuit.run
def main():


    btnAngleInc= Button(12)

    angle =0

    while True:

        #if btnAngleInc.is_pressed:
        angle += 0.20

        Servo.value= angle

        if angle == 1:
            angle=0

        sleep(.05)
