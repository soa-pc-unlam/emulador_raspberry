import os
from gpiozero import LED
from time import sleep

os.environ["PIGPIO_ADDR"] = "127.0.0.1"
os.environ["PIGPIO_PORT"] = "5000"
os.environ["GPIOZERO_PIN_FACTORY"] = "pigpio"

led = LED(24)
while True:
    print ("prende")
    led.on()
    sleep(1)
    print ("apaga")
    led.off()
    sleep(1)