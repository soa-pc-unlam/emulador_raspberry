from lib.gpiozero import PWMLED, Button
from time import sleep
from lib.CircuitPlatform import Circuit_Platform



def main():
    led = PWMLED(18)
    switchLighting = Button(11)
    btnOffLed = Button(17, pull_up=False)

    ligthing=0

    while True:
        if ligthing<0.9:
            ligthing = ligthing + 0.1
        else:
            ligthing=0

        led.value = ligthing
        print("valor luz" + str(ligthing))
        sleep(1)


if __name__ == "__main__":
    #se verifica si se esta ejcutando en simulador o la Raspberry fisica.
    #Si se ejecuta en el simulador, se crea el circuito graifco qu esta en el archivo
    #Json
    Circuit_Platform.check_plataform_simulator("PWMLed.json", main)