from lib.gpiozero import Servo, Button
from lib.tkgpio import TkCircuit
from json import load
from time import sleep

with open("LCD.json", "r") as file:
    configuration = load(file)

circuit = TkCircuit(configuration)
valor = 0  # Variable global

@circuit.run
def main():
    from Adafruit_CharLCD import Adafruit_CharLCD
    from time import sleep

    lcd = Adafruit_CharLCD(2, 3, 4, 5, 6, 7, 16, 2)
    button = Button(11)

    def show_sensor_values():
        global valor
        lcd.clear()
        lcd.message(f"hola que tal {valor}")

    def button_pressed():
        global valor  # Declarar que estamos usando la variable global
        valor += 1  # Incrementar el valor
        print(f"Pressed, valor = {valor}")
        show_sensor_values()

    button.when_pressed = button_pressed


    while True:
        sleep(0.1)
