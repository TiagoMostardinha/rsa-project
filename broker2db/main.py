import dotenv
import os
import time
import common.mqttlib as mqtt


def main(ipBroker, portBroker, usernameBroker, passwordBroker):
    print(f"Service is established.\nListening MQTT Broker at {
          ipBroker}:{portBroker}.")

    subscriber = mqtt.MQTTSubscriber(
        ipBroker,
        portBroker,
        usernameBroker,
        passwordBroker
    )

    try:
        subscriber.connect()
        print("Connected to MQTT Broker.")
        subscriber.subscribe("test")

    except Exception as e:
        print(e)
        return

    while (True):
        messages = subscriber.getMessages()
        print(messages)
        time.sleep(1)
        if len(messages) > 2:
            break

    subscriber.disconnect()


if __name__ == "__main__":
    dotenv.load_dotenv("./.env")
    ipBroker = os.getenv("IP_BROKER")
    portBroker = int(os.getenv("PORT_BROKER"))
    usernameBroker = os.getenv("USERNAME_BROKER")
    passwordBroker = os.getenv("PASSWORD_BROKER")

    main(ipBroker, portBroker,  usernameBroker, passwordBroker)
