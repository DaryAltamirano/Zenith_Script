import os
from dotenv import load_dotenv
import time
import json
from supports.MysqlConnection import MysqlConnection
from supports.ConnectionRabbitMQ import ConnectionRabbitMQ
from influxdb_client import Point

from supports.MysqlConnection import MysqlConnection
from supports.InfluxDbConnection import InfluxDbConnection
from supports.ConnectionRabbitMQ import ConnectionRabbitMQ

load_dotenv()


def data_get(data, key, parse=".", default=None):
    keys = key.split(parse)
    try:
        for k in keys:
            if isinstance(data, list):
                data = data[int(k)]
            else:
                data = data[k]
        return data
    except (KeyError, IndexError, TypeError):
        return default


def callback(self, method, properties, body):
    json_object = json.loads(body)
    id_sensor = json_object["id_sensor"]

    sql = '''select format
                from sensor_driver_sensor  
                where id = {}
                LIMIT 1;'''.format(id_sensor)

    sensor_data = MysqlConnection().getData(sql=sql)

    json_sensor = json.loads(sensor_data[0][0].replace("\'", "\"")[1: len(sensor_data[0][0]) - 1])

    response = {
        "obtained_At": data_get(json_object["data"], json_sensor["obtained_At"], "$"),
        'id_sensor': id_sensor,
        "data": []
    }

    for item in json_sensor["data"]:
        response["data"].append({
            'value': data_get(json_object["data"], item['key'], "$"),
            'unit': item['unit'],
            'category': item['category']
        })
    json_object = json.loads(body)
    id_sensor = json_object["id_sensor"]

    influxdb = InfluxDbConnection()

    p = Point(json_object['data']["category"])\
        .tag("unit", json_object['data']['unit'])\
        .tag("sensor_id", id_sensor)\
        .field("value", json_object['data']['value'])

    influxdb.write_api.write(bucket=self.bucket, record=p)

def main():
    channel = ConnectionRabbitMQ().channel()
    ConnectionRabbitMQ().basicConsume(channel, callback, None)


if __name__ == "__main__":
    main()
