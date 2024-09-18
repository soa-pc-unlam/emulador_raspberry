from lib.CreateCircuit import create_circuit
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

    button1 = Button(15)
    button2 = Button(16)
    button3 = Button(17)

    button1.when_pressed = button1_pressed
    button1.when_released = button1_released
    button2.when_pressed = button2_pressed
    button2.when_released = button2_released
    button3.when_pressed = button3_pressed
    button3.when_released = button3_released


    while True:
        sleep(0.1)

create_circuit("ButtonLedN.json", main)