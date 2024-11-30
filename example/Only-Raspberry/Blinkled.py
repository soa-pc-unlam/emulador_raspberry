from time import sleep

from gpiozero import LED


import os
def main():

    led = LED(18)
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
    
    #Circuit_Platform.check_plataform_simulator("Blinkled.json", main)
    main()
