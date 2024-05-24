import dotenv
import os
from common.mqtt import MQTTPublisher, MQTTSubscriber
import logging
from models.Boat import Boat
from models.Location import Location
from models.Neighbour import Neighbour
import time
import json
from models.ControllerMessage import ControllerMessage
from common.database import Database


def main(hostInfluxDB, portInfluxDB, orgInfluxDB, tokenInfluxDB):
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s %(levelname)s\t%(message)s',
        datefmt='%H:%M:%S',
    )

    db = Database(
        hostInfluxDB,
        portInfluxDB,
        orgInfluxDB,
        tokenInfluxDB,
        logger=logging.getLogger(__name__),
    )

    msgs = [
        ControllerMessage(
            typeOfMessage="start",
            startFlag=True,
            startLocation=Location(
                id="obu2",
                x=1,
                y=1
            ),
            destLocation=Location(
                id="rsu19",
                x=8,
                y=4,
            ),
            map=[
                ["o", "o", "o", "o", "o", "o", "o", "o", "o", "o"],
                ["o", "o", "o", "o", "o", "o", "o", "o", "o", "o"],
                ["o", "o", "o", "o", "o", "o", "o", "o", "o", "o"],
                ["o", "o", "o", "o", "o", "o", "o", "o", "o", "o"],
                ["o", "o", "o", "o", "o", "o", "o", "o", "o", "o"],
                ["o", "o", "o", "o", "o", "o", "o", "o", "o", "o"],
                ["o", "o", "o", "o", "o", "o", "o", "o", "o", "o"],
                ["o", "o", "o", "o", "o", "o", "o", "o", "o", "o"],
                ["o", "o", "o", "o", "o", "o", "o", "o", "o", "o"],
                ["o", "o", "o", "o", "o", "o", "o", "o", "o", "o"]
            ],
            inRange=None,
            stopFlag=False
        ),

        ControllerMessage(
            typeOfMessage="inrange",
            startFlag=False,
            startLocation=None,
            destLocation=None,
            map=None,
            inRange=["obu2", "rsu19"],
            stopFlag=False
        ),

        ControllerMessage(
            typeOfMessage="stop",
            startFlag=False,
            startLocation=None,
            destLocation=None,
            map=None,
            inRange=None,
            stopFlag=True
        ),
    ]

    for m in msgs:
        db.writeControllerMessage("devices/controller", json.dumps(m.__json__()))

        time.sleep(1)


if __name__ == "__main__":
    dotenv.load_dotenv("./influxdb.env")
    # influxdb environment variables
    hostInfluxDB = os.getenv("DOCKER_INFLUXDB_INIT_HOST")
    portInfluxDB = int(os.getenv("DOCKER_INFLUXDB_INIT_PORT"))
    orgInfluxDB = os.getenv("DOCKER_INFLUXDB_INIT_ORG")
    tokenInfluxDB = os.getenv("DOCKER_INFLUXDB_INIT_ADMIN_TOKEN")

    main(hostInfluxDB, portInfluxDB, orgInfluxDB, tokenInfluxDB)
