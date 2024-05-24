import dotenv
import os
from common.mqtt import MQTTPublisher, MQTTSubscriber
import logging
from models.Boat import Boat
from models.Location import Location
from models.Neighbour import Neighbour
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
        Boat(
            id="rsu19",
            status="idle",
            speed=10,
            direction=45,
            location=Location(
                id="rsu19",
                x=1,
                y=1
            ),
            destination=Location(
                id="obu02",
                x=1,
                y=1
            ),
            neighbours=[
                Neighbour(
                    name="rsu20",
                    tq=10,
                    tq=Location(
                        id="rsu20",
                        x=1,
                        y=1
                    )
                ),
                Neighbour(
                    name="rsu21",
                    tq=10,
                    location=Location(
                        id="rsu21",
                        x=1,
                        y=1
                    )
                )
            ],
            transfered_files=["file1", "file2"]
        )
    ]

    for m in msgs:
        pub.publish(f'devices/{m.id}/out',m.toJSON())

    pub.disconnect()


if __name__ == "__main__":
    dotenv.load_dotenv("./.env")
    ipBroker = os.getenv("HOST_BROKER")
    portBroker = int(os.getenv("PORT_BROKER"))
    usernameBroker = os.getenv("USERNAME_BROKER")
    passwordBroker = os.getenv("PASSWORD_BROKER")

    main(ipBroker, portBroker,  usernameBroker, passwordBroker)
