from time import sleep
from lib.gpiozero import LED
from lib.CreateCircuit import create_circuit

def main():

    led = LED(21)
    while True:
        print("prende")
        led.on()
        sleep(1)
        print("apaga")
        led.off()
        sleep(1)

create_circuit("Blinkled.json", main)