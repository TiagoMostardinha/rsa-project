import influxdb_client
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
from models.Message import Message
import logging


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

    def write(self, bucket, data):

        write_api = self.client.write_api(write_options=SYNCHRONOUS)

        point = (
            Point("pi")
            .tag("boat", "boat1")
            .field("temperature", data["temperature"])
            .field("humidity", data["humidity"])
        )

        write_api.write(bucket=bucket, org=self.org, record=point)

        self.logger.info(msg=Message(
            content=f'Message written in Bucket {bucket}: {data}',
            source="InfluxDB",
        ))

    def query(self, query):
        query_api = self.client.query_api()
        tables = query_api.query(org=self.org, query=query)
        return tables
