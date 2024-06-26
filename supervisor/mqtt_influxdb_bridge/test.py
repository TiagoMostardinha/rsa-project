import time
import dotenv
import os
from common.mqtt import MQTTPublisher
import logging
from models.Boat import Boat
from models.Location import Location
from models.Neighbour import Neighbour
from models.Floater import Floater


def main(ipBroker, portBroker, usernameBroker, passwordBroker):
    logging.basicConfig(
        level=logging.DEBUG,
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
            id="obu02",
            status="idle",
            mac="00:00:00:00:00:00",
            speed=10,
            direction=45,
            location=Location(
                id="rsu19",
                x=1,
                y=1
            ),
            destination=Location(
                id="obu02",
                x=10,
                y=10
            ),
            neighbours=[
                Neighbour(
                    name="rsu20",
                    tq=10,
                    mac="00:00:00:00:00:00",
                    location=Location(
                        id="rsu20",
                        x=1,
                        y=1,
                    ),
                    last_seen=400,
                ),
                Neighbour(
                    name="rsu21",
                    tq=10,
                    mac="00:00:00:00:00:00",
                    location=Location(
                        id="rsu21",
                        x=1,
                        y=1,

                    ),
                    last_seen=1607,
                )
            ],
            transfered_files=["file1", "file2"]
        ),
        Boat(
            id="obu02",
            mac="00:00:00:00:00:00",
            status="idle",
            speed=10,
            direction=45,
            location=Location(
                id="obu02",
                x=20,
                y=19
            ),
            destination=Location(
                id="obu02",
                x=10,
                y=10
            ),
            neighbours=[
                Neighbour(
                    name="rsu20",
                    tq=10,
                    mac="00:00:00:00:00:00",
                    location=Location(
                        id="rsu20",
                        x=1,
                        y=1,
                    ),
                    last_seen=400,
                ),
                Neighbour(
                    name="rsu21",
                    tq=10,
                    mac="00:00:00:00:00:00",
                    location=Location(
                        id="rsu21",
                        x=1,
                        y=1,

                    ),
                    last_seen=1607,
                )
            ],
            transfered_files=["file1", "file2"]
        ),
        Floater(
            id="rsu19",
            mac="00:00:00:00:00:00",
            status="idle",
            location=Location(
                id="rsu19",
                x=23,
                y=18
            ),
            files_to_tranfer=["file1", "file2"]
        )


    ]

    for m in msgs:
        pub.publish(f'devices/{m.id}/out', m.toJSON())
        time.sleep(1)

    pub.disconnect()


if __name__ == "__main__":
    dotenv.load_dotenv("./.env")
    ipBroker = os.getenv("HOST_BROKER")
    portBroker = int(os.getenv("PORT_BROKER"))
    usernameBroker = os.getenv("USERNAME_BROKER")
    passwordBroker = os.getenv("PASSWORD_BROKER")

    main(ipBroker, portBroker,  usernameBroker, passwordBroker)
