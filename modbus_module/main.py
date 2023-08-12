import os
from dotenv import load_dotenv
import json
import logging
import asyncio
from supports.MysqlConnection import MysqlConnection
from supports.ConnectionRabbitMQ import ConnectionRabbitMQ
from pymodbus.client import AsyncModbusTcpClient

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

    client = AsyncModbusTcpClient("localhost")
    try:
        # Realiza una lectura de datos desde el dispositivo esclavo
        result = await client.read_coils(address=0, count=8, unit=1)
        bits = result.bits

        print("Datos leídos:", result.bits)
        # Divide la secuencia de bits en grupos de 8 bits
        byte_strings = bits.split(" ")

        # Convierte cada byte en un carácter y crea una lista de caracteres
        characters = [chr(int(byte, 2)) for byte in byte_strings]

        # Convierte la lista de caracteres en una cadena de caracteres
        text = "".join(characters)
        
        body = {
            'id_sensor': id,
            'data': text,
            'protocol': 'HTTP'
        }

        channel = ConnectionRabbitMQ().channel()
        ConnectionRabbitMQ().basicPublish(channel, json.dumps(body))
    except Exception as e:
        print("Error:", e)


    await client.connect()
    




if __name__ == "__main__":
    asyncio.run(main())


