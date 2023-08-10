import json
from aiocoap import *

from dotenv import load_dotenv
from influxdb_client import Point

from supports.MysqlConnection import MysqlConnection
from supports.InfluxDbConnection import InfluxDbConnection
from supports.ConnectionRabbitMQ import ConnectionRabbitMQ

load_dotenv()

def callback(self, method, properties, body):
    json_object = json.loads(body)
    id_sensor = json_object["id_sensor"]

    influxdb = InfluxDbConnection()

    p = Point(json_object['data']["category"])\
        .tag("unit", json_object['data']['unit'])\
        .tag("sensor_id", id_sensor)\
        .field("value", json_object['data']['value'])

    #influxdb.write_api.write(bucket=self.bucket, record=p)


def main():
    channel = ConnectionRabbitMQ().channel()
    ConnectionRabbitMQ().basicConsume(channel, callback, None)

if __name__ == "__main__":
    main()
