import dotenv
import os
from common.mqtt import MQTTSubscriber
from common.database import Database
import logging


def main(ipBroker, portBroker, usernameBroker, passwordBroker, hostInfluxDB, portInfluxDB, orgInfluxDB, tokenInfluxDB):
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s %(levelname)s\t%(message)s',
        datefmt='%H:%M:%S',
    )

    topics = [("test", 0), ("test/pi", 0)]

    sub = MQTTSubscriber(
        host=ipBroker,
        port=portBroker,
        username=usernameBroker,
        password=passwordBroker,
        logger=logging.getLogger(__name__)
    )

    sub.connect()

    db = Database(
        hostInfluxDB,
        portInfluxDB,
        orgInfluxDB,
        tokenInfluxDB,
        logger=logging.getLogger(__name__),
    )

    sub.subscribe(topics)

    while True:
        msg = sub.popMessages()

        if msg:
            db.write("devices", msg)

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
