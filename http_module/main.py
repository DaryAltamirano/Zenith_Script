import os
from dotenv import load_dotenv
from supports.ApiConsume import ApiConsume
from supports.MysqlConnection import MysqlConnection
from supports.ConnectionRabbitMQ import ConnectionRabbitMQ
import json

load_dotenv()


def main():
    id = os.getenv('ID_SENSOR')

    sql = '''select request.connection
        from sensor_driver_sensor as sensor
        inner join sensor_driver_request as request on (request.sensor_id = sensor.id) 
        inner join sensor_driver_scheduler as scheduler on (scheduler.sensor_id = sensor.id) 
        where sensor.id = {}
        LIMIT 1;'''.format(id)
    sensor_data = MysqlConnection().getData(sql=sql)
    dict = json.loads(clearData(sensor_data[0][0]))

    dict_headers = dict['headers']
    dict_params = dict['params']
    method = dict['method']
    url = dict['uri']

    data = ApiConsume().request(url, dict_params, dict_headers, method)

    body = {
        'id_sensor': id,
        'data': data,
        'protocol': 'HTTP'
    }
    channel = ConnectionRabbitMQ().channel()
    ConnectionRabbitMQ().basicPublish(channel, json.dumps(body))


def clearData(sensor_data):
    string = sensor_data.replace("\'", "\"").replace("\\", "")
    return string[1: len(string) - 1]


if __name__ == "__main__":
    main()
