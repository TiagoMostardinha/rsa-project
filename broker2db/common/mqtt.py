import paho.mqtt.client as paho
import sys

client = paho.Client()

if client.connect("localhost",1883,60) != 0:
    print("Couldn't conntect to MQTT Broker")
    sys.exit(-1)


client.publish("test/status", "Hello World from paho",0)

client.disconnect()

