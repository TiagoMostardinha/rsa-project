import dotenv
import os
from common.mqtt import MQTTSubscriber
import logging
import time


def main(ipBroker, portBroker, usernameBroker, passwordBroker):
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s %(levelname)s\t%(message)s',
        datefmt='%H:%M:%S',
    )

    topics = [("test", 0), ("test/pi")]

    sub = MQTTSubscriber(
        host=ipBroker,
        port=portBroker,
        username=usernameBroker,
        password=passwordBroker,
        logger=logging.getLogger(__name__)
    )

    sub.connect()

    while True:

        sub.subscribe(topics)
        msg = sub.popMessages()

        if msg:
            logging.info(f"Received message: {msg}")


if __name__ == "__main__":
    dotenv.load_dotenv("./.env")
    ipBroker = os.getenv("IP_BROKER")
    portBroker = int(os.getenv("PORT_BROKER"))
    usernameBroker = os.getenv("USERNAME_BROKER")
    passwordBroker = os.getenv("PASSWORD_BROKER")

    main(ipBroker, portBroker,  usernameBroker, passwordBroker)
