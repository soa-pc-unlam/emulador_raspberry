from lib.gpiozero import Servo,Button
from lib.tkgpio import TkCircuit
from json import load
from time import sleep


with open("LCD.json", "r") as file:
    configuration = load(file)

circuit = TkCircuit(configuration)
@circuit.run
def main():
    from Adafruit_CharLCD import Adafruit_CharLCD
    from time import sleep

    lcd = Adafruit_CharLCD(2, 3, 4, 5, 6, 7, 16, 2)

    def show_sensor_values():
        lcd.clear()
        lcd.message("hola que tal")

    show_sensor_values()
    while True:

       sleep(0.1)
