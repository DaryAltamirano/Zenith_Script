import os
from dotenv import load_dotenv
import time
from request_api.supports.ApiConsume import ApiConsume
from supports.MysqlConnection import MysqlConnection
from supports.ConnectionRabbitMQ import ConnectionRabbitMQ
import json

load_dotenv()

def main():

    id = os.getenv('ID_SENSOR')

    sql = '''select request.headers, request.params, scheduler.uri
        from sensor_driver_sensor as sensor
        inner join sensor_driver_request as request on (request.sensor_id = sensor.id) 
        inner join sensor_driver_scheduler as scheduler on (scheduler.sensor_id = sensor.id) 
        where sensor.id = {}
        LIMIT 1;'''.format(id)
    
    sensor_data = MysqlConnection().getData(sql=sql)

    dict_headers = json.loads(sensor_data[0][0])
    dict_params = json.loads(sensor_data[0][1])
    url = sensor_data[0][2]

    data = ApiConsume().request(url,dict_params, dict_headers)

    body = {
        'id_sensor' : id,
        'data' : data
    }
    channel = ConnectionRabbitMQ().channel()
    ConnectionRabbitMQ().basicPublish(channel, body)

if __name__ == "__main__":
    main()

