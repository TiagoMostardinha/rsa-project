import json
from models.ControllerMessage import ControllerMessage
from models.Location import Location
from models.Boat import Boat
from models.Floater import Floater


def getNewMessages(lastMessages, database):
    # Get All messages from 20min interval
    controllerMsgs = database.queryController(20)
    boatMessages = database.queryBoat(20)
    floaterMessages = database.queryFloater(20)

    newMsgs = []

    controllerMsgs, lastMessages = getControllerMessages(
        controllerMsgs, lastMessages)
    boatMessages, lastMessages = getBoatMessages(
        boatMessages, lastMessages)
    floaterMessages, lastMessages = getFloaterMessages(
        floaterMessages, lastMessages)

    newMsgs.extend(controllerMsgs)
    newMsgs.extend(boatMessages)
    newMsgs.extend(floaterMessages)

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


def getBoatMessages(queryMsg, lastMessages):
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


def getFloaterMessages(queryMsg, lastMessages):
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
        floaterMsg = {
            "id": msg['id'],
            "mac": msg['mac'],
            "status": msg['status'],
            "location": {
                "id": msg['location_id'],
                "x": msg['location_x'],
                "y": msg['location_y'],
            },
            "files_to_tranfer": json.loads(msg['files_to_tranfer'])
        }
        floaterMsg = Floater.fromJSON(floaterMsg)
        msgsToReturn.append(floaterMsg)

    return msgsToReturn, lastMessages
