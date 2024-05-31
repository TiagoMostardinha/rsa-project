import time
import csv
import logging
import os
import dotenv
from common.mqtt import MQTTPublisher, MQTTSubscriber
import common.utils as utils
from models.ControllerMessage import ControllerMessage
from models.Boat import Boat
from common.dijkstra import *
from models.Location import Location
import time
import csv


def csvToMap(file):
    map = []
    freeSpace = 0
    with open(file, "r") as mapReader:
        csv_reader = csv.reader(mapReader, delimiter=",")

        for row in csv_reader:
            line = []
            for square in row:
                if square == "o" or square == "x":
                    if square == "o":
                        freeSpace += 1
                    line.append(square)
                else:
                    raise Exception("Invalid map format!")
            map.append(line)

    return map, freeSpace


def main(ipBroker, portBroker, usernameBroker, passwordBroker):
    boat = Boat(
        id="rsu19",
        status="idle",
        speed=0,
        direction=0,
        location=Location(
            id="rsu19",
            x=-1,
            y=-1
        ),
        destination=Location(
            id="rsu19",
            x=-1,
            y=-1
        ),
        neighbours=[],
        transfered_files=[]
    )
    # Init config for MQTT sub and InfluxDB client
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
        id="controller-publisher",
        logger=logging.getLogger(__name__)
    )

    sub = MQTTSubscriber(
        host=ipBroker,
        port=portBroker,
        username=usernameBroker,
        password=passwordBroker,
        id="controller-subscriber",
        logger=logging.getLogger(__name__)
    )

    # Read Map
    map, freeSpace = csvToMap("map.csv")

    # Read and create the topics for MQTT
    topics = {}

    topics["in"] = [f'devices/{boat.id}/in']
    topics["out"] = [f'devices/{boat.id}/out']

    with open("./devices.csv", "r") as devices:
        csv_reader = csv.reader(devices, delimiter=",")
        for row in csv_reader:
            continue

    sub.connect()
    sub.subscribe(topics["in"])

    startFlag = False
    inRange = False
    startPosition = ()

    path = []

    i = 0

    while True:
        time.sleep(1)

        if i > 10:
            sub.disconnect()
            pub.connect()
            pub.publish(topics["out"][0], boat.toJSON())
            pub.disconnect()
            sub.connect()
            i = 0
            continue
        else:
            i += 1

        for topic in topics["in"]:
            msg = sub.popMessages(topic)

            if msg:
                if msg['typeOfMessage'] == "start":
                    startFlag = True
                    boat.location.id = msg['startLocation']['id']
                    boat.location.x = int(msg['startLocation']['x'])
                    boat.location.y = int(msg['startLocation']['y'])
                    boat.destination.id = msg['destLocation']['id']
                    boat.destination.x = int(msg['destLocation']['x'])
                    boat.destination.y = int(msg['destLocation']['y'])
                    boat.status = "idle"
                if msg['typeOfMessage'] == "stop":
                    startFlag = False
                    boat.status = "idle"
                    path = []
                if msg['typeOfMessage'] == "inRange":
                    if boat.id in msg['inrange']:
                        inRange = True

        if not startFlag:
            continue

        if not inRange:
            continue

        logging.info("In range")


if __name__ == "__main__":
    dotenv.load_dotenv("./.env")

    # Broker environment variables
    hostBroker = os.getenv("HOST_BROKER")
    portBroker = int(os.getenv("PORT_BROKER"))
    usernameBroker = os.getenv("USERNAME_BROKER")
    passwordBroker = os.getenv("PASSWORD_BROKER")

    main(hostBroker,
         portBroker,
         usernameBroker,
         passwordBroker,
         )
