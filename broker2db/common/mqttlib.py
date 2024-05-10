import paho.mqtt.client as paho
import time


class MQTT:
    def __init__(self, host, port, username, password):
        self.client = paho.Client(paho.CallbackAPIVersion.VERSION2)
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.client.username_pw_set(
            username=self.username,
            password=self.password
        )

    def connect(self):
        if self.client.connect(self.host, self.port, 60) != 0:
            raise Exception("Couldn't connect to MQTT Broker")
        self.logMessage(f'Connected to {self.host}:{self.port}')

    def disconnect(self):
        self.client.disconnect()
        self.logMessage(f'Disconnected from {self.host}:{self.port}')

    def logMessage(self, message):
        msg = f'{time.strftime("%H:%M:%S",
                               time.localtime())} - {message}'
        print(msg)


class MQTTPublisher(MQTT):
    def __init__(self, host, port, username, password):
        super().__init__(
            host,
            port,
            username,
            password
        )

    def publish(self, topic, message):
        self.client.publish(topic, message)
        self.logMessage(f'[] Message published on {topic}: {message}')


class MQTTSubscriber(MQTT):
    messages = []

    def __init__(self, host, port, username, password):
        super().__init__(
            host,
            port,
            username,
            password
        )

    def subscribe(self, topic):
        self.client.on_message = self.on_message

        self.client.subscribe(topic)
        self.client.on_message = self.on_message
        self.logMessage(f'Subscribed to {topic}')

        self.client.loop_forever()

    def on_message(self, client, userdata, msg):
        self.messages.append(msg.payload.decode('utf-8'))
        self.logMessage(f'Message received on {msg.topic}: {
                        msg.payload.decode('utf-8')}')

    def popMessage(self):
        return self.messages.pop()

    def getMessages(self):
        return self.messages
