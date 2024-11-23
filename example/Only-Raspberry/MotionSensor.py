from simu_docker_rpi.CircuitPlatform import Circuit_Platform

def main():
    from time import sleep
    from simu_docker_rpi.gpiozero import Buzzer,MotionSensor

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

if __name__ == "__main__":
    #se verifica si se esta ejcutando en simulador o la Raspberry fisica.
    #Si se ejecuta en el simulador, se crea el circuito graifco qu esta en el archivo
    #Json
    Circuit_Platform.check_plataform_simulator("MotionSensor.json", main)