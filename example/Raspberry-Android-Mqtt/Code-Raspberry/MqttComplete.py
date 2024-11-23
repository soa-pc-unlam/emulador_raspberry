import threading
import time

from simu_docker_rpi.gpiozero import LED, Button, Buzzer, PWMLED, Servo, MotionSensor
from simu_docker_rpi.CircuitPlatform import Circuit_Platform

from mqttHandler.mqttHandler import MQTTHandler

IN_MIN  = 0
IN_MAX  = 180
OUT_MIN = -1
OUT_MAX =  1


STATE_SYSTEM_OFF     = 0
STATE_WAIT_ORDEN     = 1
STATE_WAIT_NOT_MOVED = 2

EVT_CONTINUE                     =   1
EVT_SWITCH_ON                    =   2
EVT_SWITCH_OFF                   =   3
EVT_ACTIVATE_ALARM_MANUAL        =   4
EVT_DEACTIVATE_ALARM_MANUAL      =   5
EVT_OPEN_DOOR                    =   6
EVT_CLOSE_DOOR                   =   7
EVT_DETECT_MOVE                  =   8
EVT_NOT_DETECT_MOVE              =   9

TOPIC_SYSTEM_STATE  = "/system/state"
TOPIC_MOVE_STATE    = "/move/state"
TOPIC_CTRL_ALARM    = "/alarm/ctrl"
TOPIC_STATE_ALARM   = "/alarm/state"
TOPIC_CTRL_DOOR     = "/door/ctrl"
TOPIC_STATE_DOOR    = "/door/state"

#Pines Actuadores
PIN_BUZZER          =  24
PIN_LED_DOOR        =  23
PIN_LED_ALARM       =  12
PIN_SERVO           =  18

PIN_DISP_RS         =  2
PIN_DISP_EN         =  3
PIN_DISP_D4         =  4
PIN_DISP_D5         =  5
PIN_DISP_D6         =  6
PIN_DISP_D7         =  7
COLUMNS_DISP        = 16
LINES_DISP          = 2

#Pines Sensores
PIN_BUTTON_DOOR     =  26
PIN_BUTTON_ALARM    =  19
PIN_MOTION_SENSOR   =  16
PIN_SWITCH          =  20


lock_event=threading.RLock()
event=EVT_CONTINUE

#como esta variable la modifica y usar siempre el mismo hilo no se usa lock para evitar problemas
#de concunrrencia
activate_siren = False


def map_value(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

def button_door_pressed():
    global event
    aux_event=EVT_DEACTIVATE_ALARM_MANUAL

    # Verifica si existe el atributo para almacenar el tiempo de la última ejecución
    if not hasattr(button_door_pressed, "last_call_time"):
        button_door_pressed.last_call_time = 0

    if not hasattr(button_door_pressed, "state"):
        button_door_pressed.state = 0

    current_time = time.monotonic()
    elapsed_time = current_time - button_door_pressed.last_call_time

    if elapsed_time >= 0.1:
        print("botón door presionado")
        button_door_pressed.last_call_time = current_time

    if button_door_pressed.state == 0:
        aux_event=EVT_OPEN_DOOR
        button_door_pressed.state = 1
        print("Boton door on")
    else:
        aux_event=EVT_CLOSE_DOOR
        button_door_pressed.state = 0
        print("Boton Alarma off")

    with lock_event:
        event = aux_event

def button_alarm_pressed():
    global event
    aux_event=EVT_DEACTIVATE_ALARM_MANUAL

    # Verifica si existe el atributo para almacenar el tiempo de la última ejecución
    if not hasattr(button_alarm_pressed, "last_call_time"):
        button_alarm_pressed.last_call_time = 0

    if not hasattr(button_alarm_pressed, "state"):
        button_alarm_pressed.state = 0

    current_time = time.monotonic()
    elapsed_time = current_time - button_alarm_pressed.last_call_time

    if elapsed_time >= 0.1:
        print("botón buzzer presionado")
        button_alarm_pressed.last_call_time = current_time

    if button_alarm_pressed.state == 0:
        aux_event=EVT_ACTIVATE_ALARM_MANUAL
        button_alarm_pressed.state = 1
        print("Boton Alarma on")
    else:
        aux_event=EVT_DEACTIVATE_ALARM_MANUAL
        button_alarm_pressed.state = 0
        print("Boton Alarma off")

    with lock_event:
        event = aux_event

def siren_alarm(led,activate):
    global activate_siren

    activate_siren=activate

def reset_siren(led):
    led.value=0

def change_siren(led):
    global activate_siren

    if not hasattr(change_siren, "ligthing"):
        change_siren.ligthing = 0

    if activate_siren==True:
        if change_siren.ligthing < 0.9:
            change_siren.ligthing = change_siren.ligthing + 0.1
        else:
            change_siren.ligthing = 0
    else:
        change_siren.ligthing = 0

    led.value = change_siren.ligthing

# Lógica separada de los botones
def switch_moved():
    global event
    aux_event=EVT_SWITCH_OFF

    if not hasattr(switch_moved, "state"):
        switch_moved.state = 0

    if switch_moved.state == 0:
        aux_event=EVT_SWITCH_ON
        switch_moved.state = 1
        print("switch on")
    else:
        aux_event=EVT_SWITCH_OFF
        switch_moved.state = 0
        print("switch off")

    with lock_event:
        event=aux_event

def switch_on():
    global event
    with lock_event:
        event=EVT_SWITCH_ON
        print("switch on")

def switch_off():
    global event
    with lock_event:
        event=EVT_SWITCH_OFF
        print("switch off")

# Callback MQTT para controlar el LED o el buzzer
def mqtt_callback(topic, message):
    global  event
    event_aux=EVT_CONTINUE

    if topic == TOPIC_CTRL_DOOR and message == "open":
        event_aux=EVT_OPEN_DOOR
    elif topic == TOPIC_CTRL_DOOR and message == "close":
        event_aux = EVT_CLOSE_DOOR
    elif topic == TOPIC_CTRL_ALARM and message == "on":
        event_aux = EVT_ACTIVATE_ALARM_MANUAL
    elif topic == TOPIC_CTRL_ALARM and message == "off":
        event_aux = EVT_DEACTIVATE_ALARM_MANUAL
    with lock_event:
        event=event_aux

def show_message_lcd(lcd,msg):
    lcd.clear()
    lcd.message(msg)

def get_event():
    global event
    if not hasattr(get_event, "last_event"):
        get_event.last_event = EVT_CONTINUE

    with lock_event:
        if(get_event.last_event == event):
            event=EVT_CONTINUE
        get_event.last_event=event


def move_servo(servo,angle_degree):
    servo_motion_angle = map_value(angle_degree, IN_MIN, IN_MAX, OUT_MIN, OUT_MAX)
    servo.value = servo_motion_angle


def motion_no_detected():
    global event
    with lock_event:
        event=EVT_NOT_DETECT_MOVE

def motion_detected():
    global event
    with lock_event:
        event=EVT_DETECT_MOVE

def main():
    from Adafruit_CharLCD import Adafruit_CharLCD

    lcd = Adafruit_CharLCD(2, 3, 4, 5, 6, 7, 16, 2)
    led_door = LED(PIN_LED_DOOR)
    led_alarm = PWMLED(PIN_LED_ALARM)
    buzzer = Buzzer(PIN_BUZZER)
    servo = Servo(PIN_SERVO)
    motion_sensor = MotionSensor(PIN_MOTION_SENSOR)


    print(f"ID del hilo Main : {threading.get_ident()}")
    # Configuración de los botones
    button_door = Button(PIN_BUTTON_DOOR, pull_up=False)
    button_alarm = Button(PIN_BUTTON_ALARM, pull_up=False)
    switch_interruptor = Button(PIN_SWITCH,pull_up=False)

    # Inicializa el manejador MQTT
    mqtt_handler = MQTTHandler(broker='broker.emqx.io', port=1883)
    mqtt_handler.connect()

    # Suscripción a tópicos y asignación del callback MQTT
    mqtt_handler.subscribe(TOPIC_CTRL_DOOR, lambda topic, message: mqtt_callback(topic, message))
    mqtt_handler.subscribe(TOPIC_CTRL_ALARM, lambda topic, message: mqtt_callback(topic, message))

    # Configuración de callbacks de los botones con publicación en MQTT
    button_door.when_pressed = lambda: button_door_pressed()
    button_alarm.when_pressed = lambda: button_alarm_pressed()
    switch_interruptor.when_pressed =lambda: switch_on()
    switch_interruptor.when_released = lambda: switch_off()
    motion_sensor.when_motion = lambda:motion_detected()
    motion_sensor.when_no_motion = lambda: motion_no_detected()

    current_state = STATE_SYSTEM_OFF
    show_message_lcd(lcd, "Sistema Apagado")

    try:
        while True:
            get_event()

            with lock_event:
                event_aux=event

            if current_state == STATE_SYSTEM_OFF:
                if event_aux==EVT_SWITCH_ON:
                    print("Enciende Sistema")
                    show_message_lcd(lcd, "Sistema Encendido")
                    mqtt_handler.publish(TOPIC_SYSTEM_STATE,"Sistema encendido")
                    current_state=STATE_WAIT_ORDEN

                elif event_aux==EVT_CONTINUE:
                    pass

            elif current_state == STATE_WAIT_ORDEN:
                if event_aux==EVT_ACTIVATE_ALARM_MANUAL:
                    buzzer.on()
                    mqtt_handler.publish(TOPIC_STATE_ALARM,"ON")
                    siren_alarm(led_alarm,True)
                    print("Suena Alarma")
                    show_message_lcd(lcd, "Suena Alarma")

                elif event_aux==EVT_DEACTIVATE_ALARM_MANUAL:
                    buzzer.off()
                    siren_alarm(led_alarm, False)
                    mqtt_handler.publish(TOPIC_STATE_ALARM, "OFF")
                    print("sistema encendido")
                    show_message_lcd(lcd, "Sistema Encendido")

                elif event_aux==EVT_OPEN_DOOR:
                    move_servo(servo,90)
                    led_door.on()
                    mqtt_handler.publish(TOPIC_STATE_DOOR, "OPEN")
                    print("Abriendo puerta")
                    show_message_lcd(lcd, "Puerta Abierta")

                elif event_aux == EVT_CLOSE_DOOR:
                    move_servo(servo, 180)
                    led_door.off()
                    reset_siren(led_alarm)
                    mqtt_handler.publish(TOPIC_STATE_DOOR,"CLOSE")
                    print("Cerrando puerta")
                    show_message_lcd(lcd, "Puerta Cerrada")

                elif event_aux==EVT_DETECT_MOVE:
                    buzzer.on()
                    print("Movimiento detectado")
                    siren_alarm(led_alarm, True)
                    mqtt_handler.publish(TOPIC_MOVE_STATE,"Movimiento detectado")
                    show_message_lcd(lcd, "Mov. detectado")

                elif event_aux==EVT_SWITCH_OFF:
                    siren_alarm(led_alarm, False)
                    led_door.off()
                    reset_siren(led_alarm)
                    buzzer.off()
                    mqtt_handler.publish(TOPIC_SYSTEM_STATE, "Sistema Apagado")
                    print("Apaga Sistema")
                    show_message_lcd(lcd, "Sistema Apagado")
                    current_state=STATE_SYSTEM_OFF

                elif event_aux == EVT_CONTINUE:
                    change_siren(led_alarm)
                    pass

            time.sleep(0.3)

    except KeyboardInterrupt:
        print("Programa finalizado.")
        mqtt_handler.disconnect()


if __name__ == "__main__":
    try:
        Circuit_Platform.check_plataform_simulator("MqttComplete.json", main)
    except KeyboardInterrupt:
        print("Programa finalizado.")
