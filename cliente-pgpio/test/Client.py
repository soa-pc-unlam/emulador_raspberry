from lib.gpiozero import LED
from lib.gpiozero.pins.pigpio import PiGPIOFactory
from time import sleep

print("Factory")
factory = PiGPIOFactory(host='127.0.0.1', port=5000)
print("Led")
led = LED(21, pin_factory=factory)
while True:
    print ("prende")
    led.on()
    sleep(1)
    print ("apaga")
    led.off()
    sleep(1)