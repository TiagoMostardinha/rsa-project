import json
from models.ControllerMessage import ControllerMessage
from models.Location import Location
from models.Boat import Boat


def getNewMessages(lastMessages, database):
    # Get All messages from 20min interval
    controllerMsgs = database.queryController(20)
    devicesMessages = database.queryDevices(20)

    newMsgs = []

    controllerMsgs, lastMessages = getControllerMessages(
        controllerMsgs, lastMessages)
    devicesMsgs, lastMessages = getDevicesMessages(
        devicesMessages, lastMessages)

    newMsgs.extend(controllerMsgs)
    newMsgs.extend(devicesMsgs)

    return newMsgs, lastMessages


def getControllerMessages(queryMsg, lastMessages):
    receivedMsgs = {}

    # Since influxdb query columns of value. it is needed to transform a column of values to a message in a row
    for record in queryMsg:
        for i in range(len(record.records)):
            timer = str(record.records[i]["_time"])
            if timer not in receivedMsgs:
                receivedMsgs[timer] = {}
            receivedMsgs[timer][record.records[i]
                                ["_field"]] = record.records[i]["_value"]

    newMsgs = []

    for timer, msg in receivedMsgs.items():
        if (timer, msg) not in lastMessages:
            newMsgs.append(msg)
            lastMessages.append((timer, msg))

    msgsToReturn = []

    for msg in newMsgs:

        if str(msg['inRange']) == 'null':
            inRange = None
        else:
            inRange = json.loads(msg['inRange'])

        controllerMsg = ControllerMessage(
            typeOfMessage=msg['typeOfMessage'],
            inRange=inRange,
        )
        msgsToReturn.append(controllerMsg)

    return msgsToReturn, lastMessages


def getDevicesMessages(queryMsg, lastMessages):
    receivedMsgs = {}

    # Since influxdb query columns of value. it is needed to transform a column of values to a message in a row
    for record in queryMsg:
        for i in range(len(record.records)):
            timer = str(record.records[i]["_time"])
            if timer not in receivedMsgs:
                receivedMsgs[timer] = {}
            receivedMsgs[timer][record.records[i]
                                ["_field"]] = record.records[i]["_value"]
            receivedMsgs[timer]['id'] = record.records[i]["id"]

    newMsgs = []

    for timer, msg in receivedMsgs.items():
        if (timer, msg) not in lastMessages:
            newMsgs.append(msg)
            lastMessages.append((timer, msg))

    msgsToReturn = []

    for msg in newMsgs:
        boatMsg = {
            "id": msg['id'],
            "mac": msg['mac'],
            "status": msg['status'],
            "speed": msg['speed'],
            "direction": msg['direction'],
            "location": {
                "id": msg['location_id'],
                "x": msg['location_x'],
                "y": msg['location_y'],
            },
            "destination": {
                "id": msg['destination_id'],
                "x": msg['destination_x'],
                "y": msg['destination_y'],
            },
            "neighbours": json.loads(msg['neighbours']),
            "transfered_files": json.loads(msg['transfered_files'])
        }
        boatMsg = Boat.fromJSON(boatMsg)
        msgsToReturn.append(boatMsg)

    return msgsToReturn, lastMessages
