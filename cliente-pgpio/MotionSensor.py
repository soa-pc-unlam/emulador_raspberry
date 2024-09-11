from lib.tkgpio import TkCircuit
from json import load

with open("MotionSensor.json", "r") as file:
    configuration = load(file)

circuit = TkCircuit(configuration)
@circuit.run
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
