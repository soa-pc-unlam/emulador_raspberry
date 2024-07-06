from lib.tkgpio import TkCircuit
from json import load

with open("ButtonBuzzer.json", "r") as file:
    configuration = load(file)

circuit = TkCircuit(configuration)
@circuit.run
def main():
    from time import sleep
    from lib.gpiozero import LED, Button,Buzzer,MotionSensor

    #funciones
    def button1_pressed():
        led1.on()

    def button1_released():
        led1.off()

    def button2_pressed():
        led2.on()

    def button2_released():
        led2.off()

    def button3_pressed():
        buzzer.on()

    def button3_released():
        buzzer.off()

    def motion_detected():
        buzzer.on()

    def motion_no_detected():
        buzzer.off()

    #Actuadores
    led1 = LED(21)
    led2 = LED(22)
    buzzer = Buzzer(23)

    #Sensores
    button1 = Button(15)
    button2 = Button(16)
    button3 = Button(17)
    motion_sensor = MotionSensor(25)

    #Handlers
    button1.when_pressed = button1_pressed
    button1.when_released = button1_released
    button2.when_pressed = button2_pressed
    button2.when_released = button2_released
    button3.when_pressed = button3_pressed
    button3.when_released = button3_released
    motion_sensor.when_motion = motion_detected
    motion_sensor.when_no_motion = motion_no_detected

    while True:
        sleep(0.1)
