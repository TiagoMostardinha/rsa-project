import influxdb_client
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
from models.Boat import Boat
from models.Message import Message
from models.Floater import Floater
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
            Point("boat")
            .tag("id", obj.id)
            .field("mac", obj.mac)
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

    def writeControllerMessage(self, topic, data: dict):
        write_api = self.client.write_api(write_options=SYNCHRONOUS)

        if data["typeOfMessage"] in ["start", "inrange", "stop"]:
            point = (
                Point("controller")
                .field("typeOfMessage", data.get("typeOfMessage", ""))
                .field("inRange", json.dumps(data.get("inRange", "")))
            )

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

    def writeFloater(self, topic, data):
        write_api = self.client.write_api(write_options=SYNCHRONOUS)

        obj = Floater.fromJSON(data)

        point = (
            Point("floater")
            .tag("id", obj.id)
            .field("mac", obj.mac)
            .field("status", obj.status)
            .field("location_id", obj.location.id)
            .field("location_x", obj.location.x)
            .field("location_y", obj.location.y)
            .field("files_to_tranfer", json.dumps(data["files_to_tranfer"]))
        )

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

    def queryBoat(self, interval):
        queryTemplate = f"""from(bucket: "devices")
        |> range(start: -{interval}m, stop: now())
        |> filter(fn: (r) => r["id"] =~ /obu/)"""
        return self.query(queryTemplate)
    
    def queryFloater(self, interval):
        queryTemplate = f"""from(bucket: "devices")
        |> range(start: -{interval}m, stop: now())
        |> filter(fn: (r) => r["id"] =~ /rsu/)"""
        return self.query(queryTemplate)

    def queryController(self, interval):
        queryTemplate = f"""from(bucket: "devices")
        |> range(start: -{interval}m, stop: now())
        |> filter(fn: (r) => r["_measurement"] == "controller")
        """
        return self.query(queryTemplate)
