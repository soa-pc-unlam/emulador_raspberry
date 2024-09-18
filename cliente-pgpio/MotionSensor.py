from lib.tkgpio import TkCircuit
from lib.CreateCircuit import create_circuit
from json import load

def main():
    from time import sleep
    from lib.gpiozero import Buzzer,MotionSensor

    #funciones
    def motion_detected():
        buzzer.on()
        print("detecta")
    def motion_no_detected():
        buzzer.off()
        print("no detecta")

    #Actuadores
    buzzer = Buzzer(23)

    #Sensores
    motion_sensor = MotionSensor(25)

    #Handlers
    motion_sensor.when_motion = motion_detected
    motion_sensor.when_no_motion = motion_no_detected

    while True:
        sleep(0.1)

create_circuit("MotionSensor.json", main)