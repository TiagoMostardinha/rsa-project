import influxdb_client
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
from models.Message import *
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

        data = fromJSON(data)

        if isinstance(data, BoatMessage):
            point = (
                Point(data.source)
                .field("status", data.status)
                .field("speed", data.content.speed)
                .field("direction", data.content.direction)
                .field("location_x", data.content.location.x)
                .field("location_y", data.content.location.y)
                .field("transfered_files", data.content.transfered_files)
                .field("destination_x", data.destination.x)
                .field("destination_y", data.destination.y)
                .field("neighbours", str(data.content.neighbours))
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

    def queryAllDevices(interval):
        queryTemplate = f"""from(bucket: "devices")
        |> range(start: -{interval}m)"""
        return query(queryTemplate)

    def queryDevice(interval):
        pass
