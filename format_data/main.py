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

    sql = '''select sensor.format as format, equipo.name as equipo_name, equipo.equipref as equipo_ref, espacio.name as espacio_name ,espacio.spaceref as espacio_ref, zona.Tz as zone_tz, sensor.protocol, sensor.name
                from sensor_driver_sensor as sensor
                inner join sensor_driver_equip as equipo on equipo.id = sensor.equip_id
                inner join sensor_driver_space as espacio on espacio.id  = equipo.space_id
                inner join sensor_driver_zone as zona on zona.id = espacio.zone_id
                where sensor.id = {}
                LIMIT 1;'''.format(id_sensor)

    try:
        
        sensor_data = MysqlConnection().getData(sql=sql)
    
        json_sensor = json.loads(clearData(sensor_data[0][0]))
    
        for item in json_sensor:
            value = data_get(json_object['data'] , next(iter(item)), "$")
            unit = item[next(iter(item))]
            category = item['category']
            equip_name = sensor_data[0][1]
            equip_ref = sensor_data[0][2]
            space_name = sensor_data[0][3]
            space_ref = sensor_data[0][4]
            zone_tz = sensor_data[0][5]
            protocol = sensor_data[0][6]
            entity_name = sensor_data[0][7]

            influxdb = InfluxDbConnection()
            if not (value is None):
                p = Point(category) \
                    .tag("equip_name", equip_name) \
                    .tag("equip_ref", equip_ref) \
                    .tag("space_name", space_name) \
                    .tag("space_ref", space_ref) \
                    .tag("zone_tz", zone_tz) \
                    .tag("protocol", protocol) \
                    .tag("entity_name", entity_name) \
                    .tag("unit", unit) \
                    .field("value", float(value)) 

                influxdb.write_api.write(bucket=influxdb.bucket, record=p)
            print ("write data") 
    except  Exception as e:
        print("Se produjo una excepción:", e)

def clearData(sensor_data):
    string = sensor_data.replace("\'", "\"").replace("\\", "")
    return string[1: len(string) - 1]

def main():
    channel = ConnectionRabbitMQ().channel()
    ConnectionRabbitMQ().basicConsume(channel, callback, None)

if __name__ == "__main__":
    main()
