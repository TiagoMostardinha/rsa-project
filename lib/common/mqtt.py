import random
import paho.mqtt.client as mqtt
from models.Message import *
import logging
import json
import threading


class MQTT:
    id: str
    client: mqtt.Client

    def __init__(self, host: str, port: int, username: str, password: str, id: str, logger: logging.Logger):
        self.host = host
        self.port = port

        self.id = id

        self.client = mqtt.Client(
            callback_api_version=mqtt.CallbackAPIVersion.VERSION2,
            client_id=self.id
        )
        self.client.username_pw_set(
            username=username,
            password=password
        )
        self.logger = logger

    def connect(self):
        try:
            rc = self.client.connect(self.host, self.port)

            if rc != 0:
                raise Exception("Couldn't connect to MQTT Broker")

            self.logger.info(msg=Message(
                content=f'Connected to {self.host}:{self.port}',
                source='MQTT'
            ))
        except Exception:
            self.logger.error(msg=ErrorMessage(
                content=f'Couldnt connect to {self.host}:{self.port}',
                source='MQTT',
                errorVar='rc',
                errorCode=404,
            ))
            exit(-1)

    def disconnect(self):
        try:
            rc = self.client.disconnect()

            if rc != 0:
                raise Exception("Couldn't disconnect from MQTT Broker")

            self.logger.info(msg=Message(
                content=f'Disconnected from {self.host}:{self.port}',
                source='MQTT'
            ))
            self.client.loop_stop()
        except Exception:
            self.logger.error(msg=ErrorMessage(
                content=f'Couldnt disconnect from {self.host}:{self.port}',
                source='MQTT',
                errorVar='rc',
                errorCode=500,
            ))
            exit(-1)


class MQTTPublisher(MQTT):
    def __init__(self, host: str, port: int, username: str, password: str, id: str, logger: logging.Logger):
        super().__init__(
            host,
            port,
            username,
            password,
            id,
            logger
        )

    def publish(self, topic: str, message: dict):
        try:

            message = json.dumps(message)

            rs = self.client.publish(topic, message)

            if rs[0] != 0:
                raise Exception("Couldn't publish message on MQTT Broker")

            self.logger.info(msg=Message(
                content=f'Message published on {topic}: {message}',
                source='MQTT'
            ))
        except Exception:
            self.logger.error(msg=ErrorMessage(
                content=f'Couldnt publish message on {topic}: {message}',
                source='MQTT',
                errorVar='rc',
                errorCode=500,
            ))
            exit(-1)


class MQTTSubscriber(MQTT):
    messages = {}

    def __init__(self, host: str, port: int, username: str, password: str, id: str, logger: logging.Logger):
        super().__init__(
            host,
            port,
            username,
            password,
            id,
            logger
        )

    def subscribe(self, topics: list[tuple[str, int]]):
        def on_message(client, userdata, msg):
            try:
                global messages

                data = msg.payload.decode("utf-8")

                m_decode = json.loads(data)

                self.messages[msg.topic].append(m_decode)

                self.logger.info(msg=Message(
                    content=f'Message received on {msg.topic}: {msg.payload}',
                    source='MQTT'
                ))
            except Exception:
                self.logger.error(msg=ErrorMessage(
                    content=f'Invalid message format of JSON',
                    source='MQTT',
                ))

        self.client.on_message = on_message

        if isinstance(topics, str):
            self.client.subscribe((topics, 0))
            self.messages[str(topics)] = []
        else:
            for topic in topics:
                self.client.subscribe((topic, 0))
                self.messages[str(topic)] = []

        threading.Thread(target=self.client.loop_forever).start()

    def popMessages(self, topic):
        if len(self.messages.keys()) == 0:
            return None
        if len(self.messages[topic]) == 0:
            return None
        return self.messages[topic].pop()
