from time import sleep
from simu_docker_rpi.gpiozero import Button
from simu_docker_rpi.CircuitPlatform import  Circuit_Platform

def main():

    def button_pressed():
        print("Pressed")
    def button_released():
        print("Released")

    def button_pressed1():
        print("Pressed 1")

    def button_released1():
        print("Released 1")

    button = Button(8, pull_up=False)
    button1 = Button(9, pull_up=False)

    button.when_pressed = button_pressed
    button.when_released = button_released

    button1.when_pressed = button_pressed1
    button1.when_released = button_released1

    while True:
        sleep(0.1)

if __name__ == "__main__":
    #se verifica si se esta ejcutando en simulador o la Raspberry fisica.
    #Si se ejecuta en el simulador, se crea el circuito graifco qu esta en el archivo
    #Json
    Circuit_Platform.check_plataform_simulator("ButtonOnly.json", main)