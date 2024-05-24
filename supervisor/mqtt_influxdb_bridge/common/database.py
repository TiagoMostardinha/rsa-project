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

    def write(self, topic, data):
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

    def query(self, query):
        query_api = self.client.query_api()
        tables = query_api.query(org=self.org, query=query)
        return tables

    def queryAllDevices(self,interval):
        queryTemplate = f"""from(bucket: "devices")
        |> range(start: -{interval}m)"""
        return self.query(queryTemplate)

    def queryDevice(interval):
        pass
