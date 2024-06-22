from tkgpio import TkCircuit
from json import load

# Traigo la configuración
with open("Client2.json", "r") as file:
    configuration = load(file)

circuit = TkCircuit(configuration)
@circuit.run
def main():
    from time import sleep
    from gpiozero import LED

    led = LED(21)
    while True:
        print("prende")
        led.on()
        sleep(1)
        print("apaga")
        led.off()
        sleep(1)

    # def button2_pressed():
    #     led2.toggle()
    #
    # # Creo Leds
    # led1 = LED(21)
    #
    # # Creo Botones
    # button1 = Button(11)
    # button2 = Button(12)
    #
    # # Asigno eventos
    # button1.when_pressed = led1.on
    # button1.when_released = led1.off
    # button2.when_pressed = button2_pressed
    #
    # while True:
    #     sleep(0.1)