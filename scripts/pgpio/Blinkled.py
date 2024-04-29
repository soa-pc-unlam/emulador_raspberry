from gpiozero import LED
from gpiozero.pins.pigpio import PiGPIOFactory
from time import sleep

factory = PiGPIOFactory(host='192.168.235.25')
led = LED(24, pin_factory=factory)

while True:
    print ("prende")
    led.on()
    sleep(1)
    print ("apaga")
    led.off()
    sleep(1)