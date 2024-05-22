import dotenv
import os
from common.mqtt import MQTTPublisher, MQTTSubscriber
from models.Message import *
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
        id="publisher",
        logger=logging.getLogger(__name__)
    )

    pub.connect()

    msgs = [
        BoatMessage(
            source="obu02",
            destination=View(x=0, y=0),
            status="active",
            content=BoatContent(
                speed=10,
                direction=0,
                location=View(x=0, y=0),
                neighbours=[
                    Neighbour(name="obu10", distance=10),
                    Neighbour(name="rsu19", distance=20)
                ],
                transfered_files=0
            )
        ),
        BoatMessage(
            source="rsu19",
            destination=View(x=4, y=10),
            status="idle",
            content=BoatContent(
                speed=0,
                direction=0,
                location=View(x=4, y=10),
                neighbours=[
                    Neighbour(name="obu10", distance=10),
                    Neighbour(name="obu02", distance=20)
                ],
                transfered_files=2
            ))
    ]

    pub.publish(f'devices/{msgs[0].source}/out', toJSON(msgs[0])) 
    pub.publish(f'devices/{msgs[1].source}/out', toJSON(msgs[1]))

    pub.disconnect()


if __name__ == "__main__":
    dotenv.load_dotenv("./.env")
    ipBroker = os.getenv("HOST_BROKER")
    portBroker = int(os.getenv("PORT_BROKER"))
    usernameBroker = os.getenv("USERNAME_BROKER")
    passwordBroker = os.getenv("PASSWORD_BROKER")

    main(ipBroker, portBroker,  usernameBroker, passwordBroker)
