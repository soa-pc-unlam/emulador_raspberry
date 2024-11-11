from time import sleep
from lib.gpiozero import Motor, Button
from lib.CircuitPlatform import Circuit_Platform
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


if __name__ == "__main__":
    #se verifica si se esta ejcutando en simulador o la Raspberry fisica.
    #Si se ejecuta en el simulador, se crea el circuito graifco qu esta en el archivo
    #Json
    Circuit_Platform.check_plataform_simulator("ButtonMotor.json", main)