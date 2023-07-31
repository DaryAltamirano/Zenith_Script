import os
from dotenv import load_dotenv
import time
import json
from supports.MysqlConnection import MysqlConnection
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

    channel = ConnectionRabbitMQ().channel()
    ConnectionRabbitMQ().basicPublish(channel, json.dumps(response))


def main():
    channel = ConnectionRabbitMQ().channel()
    ConnectionRabbitMQ().basicConsume(channel, callback, None)


if __name__ == "__main__":
    main()
