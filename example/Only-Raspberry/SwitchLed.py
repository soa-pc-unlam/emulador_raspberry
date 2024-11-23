from time import sleep
from simu_docker_rpi.gpiozero import LED, Button

from simu_docker_rpi.CircuitPlatform import Circuit_Platform


def main():
    def button_pressed():
        print("presiona boton")
        led.on()
    def button_released():
        print("suelta boton")
        led.off()

    led = LED(17)
    button = Button(22, pull_up=False)

    button.when_pressed = button_pressed
    button.when_released = button_released

    while True:
        sleep(0.1)

if __name__ == "__main__":
    #se verifica si se esta ejcutando en simulador o la Raspberry fisica.
    #Si se ejecuta en el simulador, se crea el circuito graifco qu esta en el archivo
    #Json
    Circuit_Platform.check_plataform_simulator("SwitchLed.json", main)