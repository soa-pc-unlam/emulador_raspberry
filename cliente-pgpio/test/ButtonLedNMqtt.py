from lib.CreateCircuit import create_circuit
from time import sleep
from lib.gpiozero import LED, Button
import random
from paho.mqtt import client as mqtt_client

broker = 'broker.emqx.io'
port = 1883
topicSubscribe = "/casa/boton"
topicPublish = "/casa/temperatura"

client_id = f'subscribe-{random.randint(0, 100)}'


def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print(f"Failed to connect, return code {rc}")

    client = mqtt_client.Client(mqtt_client.CallbackAPIVersion.VERSION1, client_id)
    client.on_connect = on_connect
    client.connect(broker, port)

    return client


def subscribe(client):
    def on_message(client, userdata, msg):
        print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")

    client.subscribe(topicSubscribe)
    client.on_message = on_message


def publish(client, msg):
    result = client.publish(topicPublish, msg)
    status = result.rc  # Cambié la forma de obtener el código de retorno
    if status == mqtt_client.MQTT_ERR_SUCCESS:
        print(f"Send `{msg}` to topic `{topicPublish}`")
    else:
        print(f"Failed to send message to topic {topicPublish}")


def main():
    client = connect_mqtt()
    subscribe(client)

    led1 = LED(21)
    button1 = Button(15, pull_up=False)

    def button1_pressed():
        led1.on()
        publish(client, "1")

    def button1_released():
        led1.off()
        publish(client, "0")

    button1.when_pressed = button1_pressed
    button1.when_released = button1_released

    client.loop_start()  # Start the loop in a non-blocking way

    try:
        while True:
            sleep(1)
    except KeyboardInterrupt:
        client.loop_stop()


create_circuit("ButtonLedN.json", main)
