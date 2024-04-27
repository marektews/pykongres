from random import randint
from paho.mqtt import client as mqtt_client
from threading import Thread
from time import sleep


class MQTT:
    client_id = f"pykongres-{randint(0, 1000)}"
    topic = "kw23/events"

    def __init__(self, app, production):
        self.app = app

        if production:
            # production mode
            self.broker = app.config['MQTT_BROKER_HOST']
            self.port = app.config['MQTT_BROKER_PORT']
            self.username = app.config['MQTT_BROKER_USERNAME']
            self.password = app.config['MQTT_BROKER_PASSWORD']
        else:
            # developer mode
            self.broker = 'kw23.ddns.net'
            self.port = 8883
            self.username = 'api'
            self.password = 'matuzalem'

        self.client = mqtt_client.Client(self.client_id, userdata=self, transport="tcp", protocol=mqtt_client.MQTTv311)
        # self.client.on_log = self.on_log
        self.client.on_connect = self.on_connect
        # self.client.on_message = self.on_message
        if self.username is not None:
            self.client.username_pw_set(username=self.username, password=self.password)
        self.client.connect(host=self.broker, port=self.port)
        self.client.loop_start()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.client.loop_stop(force=True)

    @staticmethod
    def on_log(client, userdata, level, buf):
        _self = userdata
        _self.app.logger.info(f"MQTT: log: level={level}, buf={buf}")
        print(f"MQTT: log: level={level}, buf={buf}")

    @staticmethod
    def on_connect(client, userdata, flags, result):
        _self = userdata
        _self.app.logger.info(f"MQTT: connected: flags={flags}, result={result}")
        print(f"MQTT: connected: flags={flags}, result={result}")
        client.subscribe(_self.topic)

    @staticmethod
    def on_message(client, userdata, message):
        _self = userdata
        _self.app.logger.info(f"MQTT: receive message={message.payload}")
        print(f"MQTT: receive message={message.payload}")

    def publish(self, data: str):
        self.client.publish(self.topic, payload=data)


# singleton do komunikacji przez brokera MQTT
mqttClient = None


def thread_routine(app, production):
    global mqttClient
    sleep(3)
    mqttClient = MQTT(app, production)


def init_mqtt(app, production):
    # wątek opóźnia o parę sekund start klienta MQTT
    th = Thread(target=thread_routine, args=(app, production,))
    th.start()


def mqtt_publish(data):
    if mqttClient is not None:
        if isinstance(data, dict):
            mqttClient.publish(str(data))
        else:
            mqttClient.publish(data)
