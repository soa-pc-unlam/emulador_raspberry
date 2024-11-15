
from simu_docker_rpi.gpiozero import Button
from simu_docker_rpi.CircuitPlatform import Circuit_Platform
from time import sleep

valor = 0
def main():
    from Adafruit_CharLCD import Adafruit_CharLCD

    lcd = Adafruit_CharLCD(2, 3, 4, 5, 6, 7, 16, 2)
    button = Button(11, pull_up=False)

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

if __name__ == "__main__":
    #se verifica si se esta ejcutando en simulador o la Raspberry fisica.
    #Si se ejecuta en el simulador, se crea el circuito graifco qu esta en el archivo
    #Json
    Circuit_Platform.check_plataform_simulator("LCD.json", main)