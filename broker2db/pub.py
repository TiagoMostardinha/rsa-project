import common.mqttlib as mqtt
import dotenv
import os
import time

dotenv.load_dotenv("./.env")
ipBroker = os.getenv("IP_BROKER")
portBroker = int(os.getenv("PORT_BROKER"))
usernameBroker = os.getenv("USERNAME_BROKER")
passwordBroker = os.getenv("PASSWORD_BROKER")

pub = mqtt.MQTTPublisher(
        ipBroker,
        portBroker,
        usernameBroker,
        passwordBroker
)

try:
    pub.connect()
    pub.publish("test","ola do pub")
except Exception as e:
    print(e)

pub.disconnect()
