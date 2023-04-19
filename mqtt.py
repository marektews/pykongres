from random import randint
from paho.mqtt import client as mqtt_client


class MQTT:
    broker = '127.0.0.1'
    port = 1883
    client_id = f"python-mqtt-{randint(0, 1000)}"
    topic = "events"

    def __init__(self):
        self.client = mqtt_client.Client(self.client_id, userdata=self)
        self.client.on_log = self.on_log
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.connect(host=self.broker, port=self.port, clean_start=True)
        self.client.loop_forever()

    @staticmethod
    def on_log(client, userdata, level, buf):
        print(f"level={level}, buf={buf}")

    @staticmethod
    def on_connect(client, userdata, flags, rc):
        _self = userdata

    @staticmethod
    def on_message(client, userdata, message):
        _self = userdata
