import time
import csv
import logging
import os
import dotenv
from common.mqtt import MQTTPublisher, MQTTSubscriber
from models.Floater import Floater
from models.Location import Location
from common.socketAPI import *
from scapy.all import get_if_hwaddr
import time
import csv
import paho.mqtt.client as mqtt
import threading


messages = {}

def main(ipBroker, portBroker, usernameBroker, passwordBroker, host_id):
    floater = Floater(
        id=host_id,
        mac="",
        status="idle",
        location=Location(host_id, -1, -1),
        files_to_tranfer=["rsu19_f1.txt", "rsu19_f2.txt"],
    )

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

    floater.mac = get_if_hwaddr("bat0")

    # Read and create the topics for MQTT
    topics = {}

    topics["in"] = [f'devices/{floater.id}/in']
    topics["out"] = [f'devices/{floater.id}/out']

    with open("./devices.csv", "r") as devices:
        csv_reader = csv.reader(devices, delimiter=",")
        for row in csv_reader:
            if row[0] == floater.id:
                floater.location.x = int(row[1])
                floater.location.y = int(row[2])

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
            
    def popMessages(topic):
        if len(messages.keys()) == 0:
            return None
        if len(messages[topic]) == 0:
            return None
        return messages[topic].pop()

    startFlag = False
    stopFlag = False
    inRange = False

    lastMessage = None

    while True:
        msg = popMessages(str(topics["in"][0]))

        if msg is None:
            continue

        if msg["typeOfMessage"] == "start":
            startFlag = True

        if msg["typeOfMessage"] == "stop":
            stopFlag = True

        if msg["typeOfMessage"] == "inrange":
            floater.status = "exchange"
            inRange = True

        if not startFlag:
            continue

        if stopFlag:
            return

        pub.connect()
        pub.publish(topics["out"][0], floater.toJSON())
        pub.disconnect()
        time.sleep(1)

        if msg == lastMessage:
            continue

        if inRange:
            socket = SocketAPI(10119, '', logging.getLogger(__name__))
            socket.socketServer(floater.files_to_tranfer)
            inRange = False
            floater.status = "idle"
            lastMessage = msg

        


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
