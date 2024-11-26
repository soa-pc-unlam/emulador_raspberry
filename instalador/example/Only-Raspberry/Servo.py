from simu_docker_rpi.gpiozero import Servo,Button

from simu_docker_rpi.CircuitPlatform import Circuit_Platform
from time import sleep


IN_MIN  = 0
IN_MAX  = 180
OUT_MIN = -1
OUT_MAX =  1
INCREMENT= 10

def map_value(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

def main():
    servo = Servo(18)
    angle_degree=0
    servo_motion_angle=0

    while True:

        angle_degree=angle_degree+INCREMENT
        servo_motion_angle = map_value(angle_degree,IN_MIN,IN_MAX,OUT_MIN,OUT_MAX)

        servo.value=servo_motion_angle
        print("\nangulo:  " + str(angle_degree))
        print("\nmotion: " + str(servo_motion_angle))

        sleep(0.5)

        if(angle_degree==180):
            angle_degree=0


if __name__ == "__main__":
    #se verifica si se esta ejcutando en simulador o la Raspberry fisica.
    #Si se ejecuta en el simulador, se crea el circuito graifco qu esta en el archivo
    #Json
    Circuit_Platform.check_plataform_simulator("Servo.json", main)