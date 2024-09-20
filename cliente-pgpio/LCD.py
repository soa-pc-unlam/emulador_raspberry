from lib.gpiozero import Button
from lib.CreateCircuit import create_circuit
from time import sleep

valor = 0
def main():
    from Adafruit_CharLCD import Adafruit_CharLCD

    lcd = Adafruit_CharLCD(2, 3, 4, 5, 6, 7, 16, 2)
    button = Button(11)

    def show_sensor_values():
        global valor
        lcd.clear()
        lcd.message(f"hola que tal {valor}")

    def button_pressed():
        global valor
        valor += 1  # Incrementar el valor
        print(f"Pressed, valor = {valor}")
        show_sensor_values()

    button.when_pressed = button_pressed

    while True:
        sleep(0.1)

create_circuit("LCD.json", main)