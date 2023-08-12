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

    protocol = await Context.create_client_context()

    request = Message(code="GET", uri='coap://localhost/time')

    try:
        response = await protocol.request(request).response

        body = {
            'id_sensor': id,
            'data': response.payload,
            'protocol': 'HTTP'
        }

        channel = ConnectionRabbitMQ().channel()
        ConnectionRabbitMQ().basicPublish(channel, json.dumps(body))
    except Exception as e:
        print('Failed to fetch resource:')
        print(e)
    else:
        print('Result: %s\n%r'%(response.code, response.payload))

if __name__ == "__main__":
    asyncio.run(main())