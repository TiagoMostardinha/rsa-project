import dotenv
import os
from common.mqtt import MQTTPublisher, MQTTSubscriber
import logging
import time
import json


def main(ipBroker, portBroker, usernameBroker, passwordBroker):
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s %(levelname)s\t%(message)s',
        datefmt='%H:%M:%S',
    )

    pub = MQTTPublisher(
        host=ipBroker,
        port=portBroker,
        username=usernameBroker,
        password=passwordBroker,
        logger=logging.getLogger(__name__)
    )

    pub.connect()
    msg = {
        "temperature": 25,
        "humidity": 50
    }
    pub.publish("test", json.dumps(msg))
    


    pub.disconnect()


if __name__ == "__main__":
    dotenv.load_dotenv("./.env")
    ipBroker = os.getenv("HOST_BROKER")
    portBroker = int(os.getenv("PORT_BROKER"))
    usernameBroker = os.getenv("USERNAME_BROKER")
    passwordBroker = os.getenv("PASSWORD_BROKER")

    main(ipBroker, portBroker,  usernameBroker, passwordBroker)
