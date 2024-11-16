from time import sleep
from simu_docker_rpi.gpiozero import LED, Button, Buzzer
from simu_docker_rpi.CircuitPlatform import Circuit_Platform
from mqttHandler.mqttHandler import MQTTHandler

TOPIC_BTN_BUZZER = "/button/buzzer"
TOPIC_BTN_LED = "/button/led"
TOPIC_CTRL_BUZZER = "/control/buzzer"
TOPIC_CTRL_LED = "/control/led"

# Lógica separada de los botones
def button1_pressed(led, mqtt_handler):
    led.on()
    mqtt_handler.publish(TOPIC_BTN_LED, "presionado")


def button1_released(led, mqtt_handler):
    led.off()
    mqtt_handler.publish(TOPIC_BTN_LED, "liberado")


def button3_pressed(buzzer, mqtt_handler):
    print("prende")
    buzzer.on()
    mqtt_handler.publish(TOPIC_BTN_BUZZER, "presionado")


def button3_released(buzzer, mqtt_handler):
    print("apaga")
    buzzer.off()
    mqtt_handler.publish(TOPIC_BTN_BUZZER, "liberado")


# Callback MQTT para controlar el LED o el buzzer
def mqtt_callback(topic, message, led, buzzer):
    if topic == TOPIC_CTRL_LED and message == "on":
        led.on()
    elif topic == TOPIC_CTRL_LED and message == "off":
        led.off()
    elif topic == TOPIC_CTRL_BUZZER and message == "on":
        buzzer.on()
    elif topic == TOPIC_CTRL_BUZZER and message == "off":
        buzzer.off()


# Función main
def main():
    led1 = LED(21)
    buzzer = Buzzer(23)

    # Configuración de los botones
    button1 = Button(15, pull_up=False)
    button3 = Button(17, pull_up=False)

    # Inicializa el manejador MQTT
    mqtt_handler = MQTTHandler(broker='broker.emqx.io', port=1883)
    mqtt_handler.connect()

    # Suscripción a tópicos y asignación del callback MQTT
    mqtt_handler.subscribe(TOPIC_CTRL_LED, lambda topic, message: mqtt_callback(topic, message, led1, buzzer))
    mqtt_handler.subscribe(TOPIC_CTRL_BUZZER, lambda topic, message: mqtt_callback(topic, message, led1, buzzer))

    # Configuración de callbacks de los botones con publicación en MQTT
    button1.when_pressed = lambda: button1_pressed(led1, mqtt_handler)
    button1.when_released = lambda: button1_released(led1, mqtt_handler)
    button3.when_pressed = lambda: button3_pressed(buzzer, mqtt_handler)
    button3.when_released = lambda: button3_released(buzzer, mqtt_handler)

    try:
        while True:
            sleep(0.1)
    except KeyboardInterrupt:
        print("Programa finalizado.")
        mqtt_handler.disconnect()


if __name__ == "__main__":
    try:
        Circuit_Platform.check_plataform_simulator("MqttButtonBuzzer.json", main)
    except KeyboardInterrupt:
        print("Programa finalizado.")
