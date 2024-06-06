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
from common.batman import Batman
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
        id="obu02",
        mac="",
        status="idle",
        speed=0,
        direction=0,
        location=Location(
            id="obu02",
            x=-1,
            y=-1
        ),
        destination=Location(
            id="",
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
            if row[0] == boat.id:
                boat.location.x = int(row[2])
                boat.location.y = int(row[3])
                boat.destination.x = int(row[4])
                boat.destination.y = int(row[5])


    # TODO: get mac from batman

    sub.connect()
    sub.subscribe(topics["in"])

    startFlag = False
    inRange = False
    startPosition = (boat.location.x,boat.location.y)

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
                    boat.status = "moving"
                    startPosition = (boat.location.x, boat.location.y)
                    graph = mapToGraph(map)
                    path = shortestPath(n=freeSpace, edges=graph, src=(
                        boat.location.y, boat.location.x), target=(boat.destination.y, boat.destination.x))
                if msg['typeOfMessage'] == "stop":
                    startFlag = False
                    boat.status = "idle"
                    path = []
                if msg['typeOfMessage'] == "inRange":
                    if boat.id in msg['inrange']:
                        inRange = True
                        path = shortestPath(n=freeSpace, edges=graph, src=(
                            startPosition[1], startPosition[0]), target=(
                            boat.location.y, boat.location.x))

        if not startFlag:
            continue

        if len(path) <= 0:
            continue

        coord = path.pop(0)
        boat.location.x = coord[1]
        boat.location.y = coord[0]

        logging.info(
            f"Boat {boat.id} is at {boat.location.x}, {boat.location.y}")

        if not inRange:
            continue
        
        # TODO: open socket with rsu

        # if tq < 210:
        # if tq > 240:
        # if tq < 200: find new path

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
