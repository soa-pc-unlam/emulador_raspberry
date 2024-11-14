from time import sleep

from simu_docker_rpi.CircuitPlatform import Circuit_Platform
from simu_docker_rpi.gpiozero import LED
#from lib.gpiozero import LED
#from lib.CircuitPlatform import Circuit_Platform

import os
def main():

    led = LED(17)
    while True:
        print("prende")
        led.on()
        sleep(1)
        print("apaga")
        led.off()
        sleep(1)


if __name__ == "__main__":
    #se verifica si se esta ejcutando en simulador o la Raspberry fisica.
    #Si se ejecuta en el simulador, se crea el circuito graifco qu esta en el archivo
    #Json
    current_dir = os.path.dirname(os.path.abspath(__file__))
    nameFileJson = os.path.join(current_dir, "Blinkled.json")

    Circuit_Platform.check_plataform_simulator(nameFileJson, main)