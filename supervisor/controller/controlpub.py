import dotenv
import os
import logging
from models.Boat import Boat
from models.Location import Location
from models.Neighbour import Neighbour
from models.ControllerMessage import ControllerMessage
from common.database import Database


def main(hostInfluxDB, portInfluxDB, orgInfluxDB, tokenInfluxDB):
    logging.basicConfig(
        level=logging.DEBUG,
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
                id="obu02",
                x=0,
                y=0
            ),
            destLocation=Location(
                id="rsu19",
                x=28,
                y=18,
            ),
            inRange=None,
            stopFlag=False
        ),
        ControllerMessage(
            typeOfMessage="stop",
            startFlag=False,
            startLocation=None,
            destLocation=None,
            inRange=None,
            stopFlag=True
        ),
    ]

    for m in msgs:
        db.writeControllerMessage("devices/controller", m.__json__())


if __name__ == "__main__":
    dotenv.load_dotenv("./influxdb.env")
    # influxdb environment variables
    hostInfluxDB = os.getenv("DOCKER_INFLUXDB_INIT_HOST")
    portInfluxDB = int(os.getenv("DOCKER_INFLUXDB_INIT_PORT"))
    orgInfluxDB = os.getenv("DOCKER_INFLUXDB_INIT_ORG")
    tokenInfluxDB = os.getenv("DOCKER_INFLUXDB_INIT_ADMIN_TOKEN")

    main(hostInfluxDB, portInfluxDB, orgInfluxDB, tokenInfluxDB)
