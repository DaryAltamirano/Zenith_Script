import os

from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS


class InfluxDbConnection:

    def __init__(self):

        self.url = os.getenv('INFLUX_URL')
        self.token = os.getenv('INFLUX_TOKEN')
        self.org = os.getenv('INFLUX_ORG')
        self.bucket = os.getenv('INFLUX_BUCKET')

        client = InfluxDBClient(url=self.url, token=self.token, org=self.org)
        self.write_api = client.write_api(write_options=SYNCHRONOUS)

