import dotenv
import os
from common.mqtt import MQTTSubscriber,MQTTPublisher
from common.database import Database
import logging
import csv


def main(ipBroker, portBroker, usernameBroker, passwordBroker, hostInfluxDB, portInfluxDB, orgInfluxDB, tokenInfluxDB):
    # Init config for MQTT sub and InfluxDB client
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


    # Read and create the topics for MQTT
    topics = []

    with open("./devices.csv", "r") as devices:
        csv_reader = csv.reader(devices, delimiter=",")
        for row in csv_reader:
            topics.append(f'devices/{row[0]}/in')
    
    # Read Map
    map = []
    with open("./map.csv","r") as mapReader:
        csv_reader = csv.reader(mapReader, delimiter=",")

        for row in csv_reader:
            line = []
            for square in row:
                if square == "o" or square == "x":
                    line.append(square)
                else:
                    logging.error("Invalid map format!")
                    exit(-1)
            map.append(line)

    


    # Connect to MQTT Broker
    pub.connect()

    i = True


    


    while True:
        if i:
            i = False
            pub.publish(topics[0],{"map":map})

    


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
