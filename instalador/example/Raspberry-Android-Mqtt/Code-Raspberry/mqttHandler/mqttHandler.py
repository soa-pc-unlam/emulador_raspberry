import random

from paho.mqtt import client as mqtt


class MQTTHandler:
    def __init__(self, broker, port=1883):
        self.broker = broker
        self.port = port
        self.client_id = f'python-mqtt-{random.randint(0, 1000)}'
        self.client = mqtt.Client()
        self.username = ''
        self.password = ''

        self.subscribers = {}

        # Establezco los MQTT callbacks
        self.client.on_connect = self._on_connect
        self.client.on_message = self._on_message

    def _on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT broker")
        else:
            print(f"Failed to connect, return code {rc}")

    def _on_message(self, client, userdata, msg):
        topic = msg.topic
        message = msg.payload.decode("utf-8")
        if topic in self.subscribers:
            for callback in self.subscribers[topic]:
                callback(topic, message)

    def connect(self):
        self.client.connect(self.broker, self.port)
        self.client.loop_start()

    def disconnect(self):
        self.client.loop_stop()
        self.client.disconnect()

    def subscribe(self, topic, callback):
        """se subscribe a un topico  registra un callback que va a ser llamado cuando se reciba
        un mensaje en ese topcio"""

        if topic not in self.subscribers:
            self.subscribers[topic] = []
            self.client.subscribe(topic)

        self.subscribers[topic].append(callback)

    def publish(self, topic, message):
        """"Publica un mensaje en un un topcio"""
        self.client.publish(topic, message)
