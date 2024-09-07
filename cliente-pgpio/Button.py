from lib.tkgpio.tkgpio import TkCircuit
from json import load
from time import sleep
from lib.gpiozero import Button


'''definicion de funciones'''
def button_pressed():
    print("Pressed")

def button_released():
    print("Released")


def main():

    button = Button(11)

    button.when_pressed = button_pressed
    button.when_released = button_released

    while True:
        sleep(0.1)


def create_circuit():
    '''Zona donde se crea el circuito gráfico'''
    with open("Button.json", "r") as file:
        configuration = load(file)

    circuit = TkCircuit(configuration)

    # Usar el decorador @circuit.run con la función main
    circuit.run(main)

create_circuit()