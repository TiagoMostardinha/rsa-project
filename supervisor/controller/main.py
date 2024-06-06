import time
import csv
import logging
import os
import dotenv
from common.mqtt import MQTTPublisher
from common.database import Database
import common.utils as utils
from models.ControllerMessage import ControllerMessage
from models.Boat import Boat


def main(ipBroker, portBroker, usernameBroker, passwordBroker, hostInfluxDB, portInfluxDB, orgInfluxDB, tokenInfluxDB):
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

    db = Database(
        hostInfluxDB,
        portInfluxDB,
        orgInfluxDB,
        tokenInfluxDB,
        logger=logging.getLogger(__name__),
    )

    # Range of floater and boats
    rangeOfDevices = 5

    # Read and create the topics for MQTT
    devices = {}

    with open("./devices.csv", "r") as devicesFile:
        csv_reader = csv.reader(devicesFile, delimiter=",")
        for row in csv_reader:
            devices[row[0]] = {
                "id": row[0],
                "device": None,
                "topic": f'devices/{row[0]}/in',
            }

    # Read Map
    originalMap = []
    with open("./map.csv", "r") as mapReader:
        csv_reader = csv.reader(mapReader, delimiter=",")

        for row in csv_reader:
            line = []
            for square in row:
                if square == "o" or square == "x":
                    line.append(square)
                else:
                    logging.error("Invalid map format!")
                    exit(-1)
            originalMap.append(line)

    map = originalMap.copy()

    # Connect to MQTT Broker

    time.sleep(5)

    lastMessages = []

    while True:
        newMsgs, lastMessages = utils.getNewMessages(lastMessages, db)

        if len(newMsgs) <= 0:
            continue

        logging.info(f"New messages: {newMsgs}")

        # Process messages
        for msg in newMsgs:
            if isinstance(msg, Boat):
                if devices[msg.id]["device"] != None:
                    map[devices[msg.id]["device"].location.y][devices[msg.id]
                                                              ["device"].location.x] = "o"
                devices[msg.id]["device"] = msg
                if "obu" in msg.id:
                    map[msg.location.y][msg.location.x] = "b"
                if "rsu" in msg.id:
                    map[msg.location.y][msg.location.x] = "f"

            if isinstance(msg, ControllerMessage):
                pub.connect()
                if msg.typeOfMessage == "start":
                    for dev in devices.keys():
                        pub.publish(devices[dev]
                            ["topic"], msg.__json__())
                if msg.typeOfMessage == "stop":
                    for dev in devices.values():
                        pub.publish(dev["topic"], msg.__json__())
                pub.disconnect()


        for id, dev in devices.items():
                
            if "rsu" not in id or not dev["device"] or dev["device"].location.x < 0 or dev["device"].location.y < 0:
                continue
            for i, d in devices.items():
                if "rsu" in i or not d["device"] or d["device"].location.x < 0 or d["device"].location.y < 0:
                    continue
                if (abs(dev["device"].location.x - d["device"].location.x) <= rangeOfDevices
                        or abs(dev["device"].location.y - d["device"].location.y) <= rangeOfDevices):
                    controllerMsg = ControllerMessage(
                        typeOfMessage="inrange",
                        inRange=[id,i],
                    )
                    pub.connect()
                    pub.publish(dev["topic"],controllerMsg.__json__())
                    pub.publish(d["topic"],controllerMsg.__json__())
                    pub.disconnect()
                    

        time.sleep(1)


if __name__ == "__main__":
    dotenv.load_dotenv("./.env")

    # Broker environment variables
    hostBroker = os.getenv("HOST_BROKER")
    portBroker = int(os.getenv("PORT_BROKER"))
    usernameBroker = os.getenv("USERNAME_BROKER")
    passwordBroker = os.getenv("PASSWORD_BROKER")

    dotenv.load_dotenv("./influxdb.env")
    # influxdb environment variables
    hostInfluxDB = os.getenv("DOCKER_INFLUXDB_INIT_HOST")
    portInfluxDB = int(os.getenv("DOCKER_INFLUXDB_INIT_PORT"))
    orgInfluxDB = os.getenv("DOCKER_INFLUXDB_INIT_ORG")
    tokenInfluxDB = os.getenv("DOCKER_INFLUXDB_INIT_ADMIN_TOKEN")

    main(hostBroker,
         portBroker,
         usernameBroker,
         passwordBroker,
         hostInfluxDB,
         portInfluxDB,
         orgInfluxDB,
         tokenInfluxDB
         )
