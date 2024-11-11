from lib.CircuitPlatform import Circuit_Platform
from time import sleep
from lib.gpiozero import LED, Button

def main():

    def button1_pressed():
        led1.on()

    def button1_released():
        led1.off()

    def button2_pressed():
        led2.on()

    def button2_released():
        led2.off()

    def button3_pressed():
        led3.on()

    def button3_released():
        led3.off()

    led1 = LED(21)
    led2 = LED(22)
    led3 = LED(23)

    button1 = Button(15, pull_up=False)
    button2 = Button(16, pull_up=False)
    button3 = Button(17, pull_up=False)

    button1.when_pressed = button1_pressed
    button1.when_released = button1_released
    button2.when_pressed = button2_pressed
    button2.when_released = button2_released
    button3.when_pressed = button3_pressed
    button3.when_released = button3_released


    while True:
        sleep(0.1)

if __name__ == "__main__":
    #se verifica si se esta ejcutando en simulador o la Raspberry fisica.
    #Si se ejecuta en el simulador, se crea el circuito graifco qu esta en el archivo
    #Json
    Circuit_Platform.check_plataform_simulator("ButtonLedN.json", main)