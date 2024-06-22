import dotenv
import os
from common.mqtt import MQTTSubscriber
from common.database import Database
import logging
import csv


def main(ipBroker, portBroker, usernameBroker, passwordBroker, hostInfluxDB, portInfluxDB, orgInfluxDB, tokenInfluxDB):
    # Init config for MQTT sub and InfluxDB client
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s %(levelname)s\t%(message)s',
        datefmt='%H:%M:%S',
    )

    sub = MQTTSubscriber(
        host=ipBroker,
        port=portBroker,
        username=usernameBroker,
        password=passwordBroker,
        id="mqtt-influxdb-bridge-subscriber",
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
            topics.append(f'devices/{row[0]}/out')

    # Connect to MQTT Broker
    sub.connect()

    # Listens to topics in MQTT Broker
    sub.subscribe(topics)

    while True:
        # Loop for new message in topics and write in bucket devices
        for topic in topics:
            msg = sub.popMessages(topic)

            if msg:
                try:
                    db.writeBoat(topic, msg)
                except Exception as e:
                    logging.info(e)
                    db.writeFloater(topic, msg)

    sub.disconnect()


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
