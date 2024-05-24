import influxdb_client
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
from models.Boat import Boat
from models.Message import Message
import logging
import json


class Database:
    def __init__(self, hostInfluxdb, portInfluxdb, orgInfluxdb, tokenInfluxdb, logger: logging.Logger) -> None:
        self.host = hostInfluxdb
        self.port = portInfluxdb
        self.org = orgInfluxdb
        self.token = tokenInfluxdb

        self.client = influxdb_client.InfluxDBClient(
            url=f"http://{self.host}:{self.port}",
            token=self.token,
            org=self.org
        )

        self.logger = logger

        self.logger.info(msg=Message(
            content=f'Connected to InfluxDB: org={self.org}',
            source="InfluxDB",
        ))

    def writeBoat(self, topic, data):
        write_api = self.client.write_api(write_options=SYNCHRONOUS)

        obj = Boat.fromJSON(data)

        point = (
            Point(obj.id)
            .field("status", obj.status)
            .field("speed", obj.speed)
            .field("direction", obj.direction)
            .field("location_id", obj.location.id)
            .field("location_x", obj.location.x)
            .field("location_y", obj.location.y)
            .field("destination_id", obj.destination.id)
            .field("destination_x", obj.destination.x)
            .field("destination_y", obj.destination.y)
            .field("neighbours", json.dumps(data["neighbours"]))
            .field("transfered_files", json.dumps(data["transfered_files"]))
        )

        bucket = topic.split("/")[0]
        write_api.write(bucket=bucket, org=self.org, record=point)

        self.logger.info(msg=Message(
            content=f'Message written in Bucket {bucket}: {data}',
            source="InfluxDB",
        ))

    def writeControllerMessage(self, topic, data):
        write_api = self.client.write_api(write_options=SYNCHRONOUS)

        data = json.loads(data)

        point = Point("controller").field(
            "typeOfMessage", data["typeOfMessage"])

        if data["typeOfMessage"] == "start":
            point.field("startFlag", data["startFlag"])
            point.field("startLocation_id", data["startLocation"]["id"])
            point.field("startLocation_x", data["startLocation"]["x"])
            point.field("startLocation_y", data["startLocation"]["y"])
            point.field("destLocation_id", data["destLocation"]["id"])
            point.field("destLocation_x", data["destLocation"]["x"])
            point.field("destLocation_y", data["destLocation"]["y"])
            point.field("map", json.dumps(data["map"]))
        elif data["typeOfMessage"] == "inrange":
            point.field("inRange", json.dumps(data["inRange"]))
        elif data["typeOfMessage"] == "stop":
            point.field("stopFlag", data["stopFlag"])
        else:
            self.logger.error(msg=Message(
                content=f'Invalid typeOfMessage: {data["typeOfMessage"]}',
                source="InfluxDB",
            ))
            return

        bucket = topic.split("/")[0]
        write_api.write(bucket=bucket, org=self.org, record=point)

        self.logger.info(msg=Message(
            content=f'Message written in Bucket {bucket}: {data}',
            source="InfluxDB",
        ))

    def query(self, query):
        query_api = self.client.query_api()
        tables = query_api.query(org=self.org, query=query)
        return tables

    def queryAllDevices(self, interval):
        queryTemplate = f"""from(bucket: "devices")
        |> range(start: -{interval}m)"""
        return self.query(queryTemplate)

    def queryController(self, interval):
        queryTemplate = f"""from(bucket: "devices")
        |> range(start: -{interval}m, stop: now())
        |> sort(columns: ["_value"], desc: true)
        |> filter(fn: (r) => r._measurement == "controller")
        """
        return self.query(queryTemplate)
