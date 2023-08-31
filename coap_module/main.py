from aiocoap import *
import os
from dotenv import load_dotenv
import json
import logging
import asyncio
from supports.MysqlConnection import MysqlConnection
from supports.ConnectionRabbitMQ import ConnectionRabbitMQ
import asyncio
from aiocoap import *
logging.basicConfig(level=logging.INFO)

load_dotenv()

async def main():

    id = os.getenv('ID_SENSOR')

    sql = '''select request.connection
        from sensor_driver_sensor as sensor
        inner join sensor_driver_request as request on (request.sensor_id = sensor.id) 
        inner join sensor_driver_scheduler as scheduler on (scheduler.sensor_id = sensor.id) 
        where sensor.id = {}
        LIMIT 1;'''.format(id)
    sensor_data = MysqlConnection().getData(sql=sql)
    dict = json.loads(clearData(sensor_data[0][0]))
    uri = dict['uri']
    method = dict['method']
    port = dict['port']

    protocol = await Context(loggername=None).create_client_context()

    if method == 'GET':
        method = GET
    elif method == 'POST':
        method = POST
    else: 
        method = GET
 
    request = Message(code=method, uri=uri)

    response = await protocol.request(request).response
    body = {
        'id_sensor': id,
        'data': json.loads(response.payload.decode()),
        'protocol': 'COAP'
    }

    channel = ConnectionRabbitMQ().channel()
    ConnectionRabbitMQ().basicPublish(channel, json.dumps(body))

def clearData(sensor_data):
    string = sensor_data.replace("\'", "\"").replace("\\", "")
    return string[1: len(string) - 1]

if __name__ == "__main__":
    asyncio.run(main())