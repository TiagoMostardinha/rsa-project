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
import threading
import time
from scapy.all import get_if_hwaddr
import csv
from common.socketAPI import SocketAPI
from models.Neighbour import Neighbour
import paho.mqtt.client as mqtt
import json

messages = {}


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


def main(ipBroker, portBroker, usernameBroker, passwordBroker, host_id):
    boat = Boat(
        id=host_id,
        mac="",
        status="idle",
        speed=0,
        direction=0,
        location=Location(
            id="host_id",
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

    boat.mac = get_if_hwaddr("bat0")

    # Read Map
    map, freeSpace = csvToMap("map.csv")
    graph = mapToGraph(map)

    # Read and create the topics for MQTT
    topics = {}
    topics["in"] = []
    topics["out"] = []
    topics["in"].append(f'devices/{boat.id}/in')
    topics["out"].append(f'devices/{boat.id}/out')

    with open("./devices.csv", "r") as devices:
        csv_reader = csv.reader(devices, delimiter=",")
        for row in csv_reader:
            if row[0] == boat.id:
                boat.location.id = row[0]
                boat.location.x = int(row[1])
                boat.location.y = int(row[2])
                boat.destination.id = row[3]
                boat.destination.x = int(row[4])
                boat.destination.y = int(row[5])

    # sub.connect()
    # sub.subscribe(topics["in"])

    def on_connect(client, userdata, flags, rc, properties):
        print("Connected with result code " + str(rc))
        client.subscribe(topics["in"][0])

    def on_message(client, userdata, msg):
        global messages
        data = msg.payload.decode("utf-8")
        logging.info(f"Message received: {data}")

        m_decode = json.loads(data)

        messages[msg.topic].append(m_decode)

    

    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    client.username_pw_set(
        username="admin",
        password="admin"
    )

    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(ipBroker, portBroker, 60)
    threading.Thread(target=client.loop_forever).start()

    if isinstance(topics["in"], str):
        client.subscribe((topics, 0))
        messages[str(topics)] = []
    else:
        for topic in topics["in"]:
            client.subscribe((topic, 0))
            messages[str(topic)] = []

    startFlag = False
    inRange = False
    stopFlag = False
    startPosition = (boat.location.x, boat.location.y)

    path = []

    lastMessage = None

    def popMessages(topic):
        if len(messages.keys()) == 0:
            return None
        if len(messages[topic]) == 0:
            return None
        return messages[topic].pop()

    while True:

        msg = popMessages(str(topics["in"][0]))

        if msg is not None:
            if msg["typeOfMessage"] == "start":
                boat.status = "moving"
                startFlag = True

            if msg["typeOfMessage"] == "stop":
                boat.status = "end"
                stopFlag = True

            if msg["typeOfMessage"] == "inrange":
                boat.status = "exchange"
                inRange = True

        time.sleep(1)

        if not startFlag:
            continue

        client.publish(topics["out"][0], json.dumps(boat.toJSON()))

        if stopFlag:
            return

        if inRange:
            if msg != lastMessage:

                socket = SocketAPI(10119, '10.1.1.10',
                                   logging.getLogger(__name__))
                boat.transfered_files = socket.clientSocket()
                inRange = False
                boat.status = "idle"
                boat.destination.x = startPosition[0]
                boat.destination.y = startPosition[1]
                path = []
                lastMessage = msg

        if len(path) <= 0:
            path = shortestPath(n=freeSpace, edges=graph, src=(
                boat.location.y, boat.location.x), target=(boat.destination.y, boat.destination.x))

        coord = path.pop(0)
        boat.location.x = coord[1]
        boat.location.y = coord[0]

        logging.info(
            f"Boat[{boat.id}]=({boat.location.x}, {boat.location.y})")

        # socketserver = SocketAPI(10119, '', logging.getLogger(__name__))

        # def send_location_data(boat, socketserver):
        #     socketserver.locationServerSocket(boat.id, boat.mac,
        #                                       boat.location.x, boat.location.y)
        #     return
        # while True:
        #     thread = threading.Thread(
        #     target=send_location_data, args=(boat, socketserver))
        #     thread.start()

        
        #     try:
        #         socketclient = SocketAPI(
        #     10102, '10.1.1.2', logging.getLogger(__name__))
        #         data = socketclient.locationClientSocket()
        #         break
        #     except Exception as e:
        #         continue
        # thread.join()

        # neighbour = Neighbour(
        #     name=data["id"],
        #     mac=data["mac"],
        #     tq=-1,
        #     location=Location(
        #         id=data["id"],
        #         x=data["x"],
        #         y=data["y"]
        #     ),
        #     last_seen=-1
        # )

        

        tq_neighbour = Batman().get_neighbours()

        # for n in tq_neighbour:
        #     if n.mac == neighbour.mac:
        #         neighbour.tq = n.tq
        #         neighbour.last_seen = n.last_seen

        #boat.neighbours.append(tq_neighbour)

        for n in tq_neighbour:
            if n.tq > 210:
                boat.location.y += 1
            if n.tq > 240:
                n.location.y -= 1

            if n.tq < 200:
                path = []

        logging.info(
            f"Boat[{boat.id}]=({boat.location.x}, {boat.location.y})")


if __name__ == "__main__":
    dotenv.load_dotenv("./.env")

    # Broker environment variables
    hostBroker = os.getenv("HOST_BROKER")
    portBroker = int(os.getenv("PORT_BROKER"))
    usernameBroker = os.getenv("USERNAME_BROKER")
    passwordBroker = os.getenv("PASSWORD_BROKER")
    host_id = os.getenv("HOST_ID")

    main(hostBroker,
         portBroker,
         usernameBroker,
         passwordBroker,
         host_id
         )
