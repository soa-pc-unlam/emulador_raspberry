from tkgpio import TkCircuit
from json import load

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