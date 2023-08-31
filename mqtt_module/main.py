import json
import logging
import os
import random
import time

from dotenv import load_dotenv

from supports.MysqlConnection import MysqlConnection
from supports.ConnectionRabbitMQ import ConnectionRabbitMQ
from paho.mqtt import client as mqtt_client

load_dotenv()

id_sensor = os.getenv('ID_SENSOR')

client_id = f'python-mqtt-{random.randint(0, 1000)}'

FIRST_RECONNECT_DELAY = 1
RECONNECT_RATE = 2

MAX_RECONNECT_COUNT = 12
MAX_RECONNECT_DELAY = 60

def on_disconnect(client, userdata, rc):
    logging.info("Disconnected with result code: %s", rc)
    reconnect_count, reconnect_delay = 0, FIRST_RECONNECT_DELAY
    while reconnect_count < MAX_RECONNECT_COUNT:
        logging.info("Reconnecting in %d seconds...", reconnect_delay)
        time.sleep(reconnect_delay)

        try:
            client.reconnect()
            logging.info("Reconnected successfully!")
            return
        except Exception as err:
            logging.error("%s. Reconnect failed. Retrying...", err)

        reconnect_delay *= RECONNECT_RATE
        reconnect_delay = min(reconnect_delay, MAX_RECONNECT_DELAY)
        reconnect_count += 1
    logging.info("Reconnect failed after %s attempts. Exiting...", reconnect_count)

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT Broker!")
    else:
        print("Failed to connect, return code %d\n", rc)

def subscribe(client: mqtt_client, topic):
    def on_message(client, userdata, msg):
        body = {
            'id_sensor': id_sensor,
            'data':  json.loads(msg.payload.decode()),
            'protocol': 'MQTT'
        }

        print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
        channel = ConnectionRabbitMQ().channel()
        ConnectionRabbitMQ().basicPublish(channel, json.dumps(body))

    client.subscribe(topic)
    client.on_message = on_message

def connect_mqtt(broker, port, username = None, password = None):

    # Set Connecting Client ID
    client = mqtt_client.Client(client_id)
    if not (username is None) and not (password is None):
        client.username_pw_set(username, password)

    client.on_connect = on_connect
    client.on_disconnect = on_disconnect

    client.connect(broker, int(port))
    return client

def clearData(sensor_data):
    string = sensor_data.replace("\'", "\"").replace("\\", "")
    return string[1: len(string) - 1]

def main():
    id = os.getenv('ID_SENSOR')

    sql = '''select request.connection
        from sensor_driver_sensor as sensor
        inner join sensor_driver_request as request on (request.sensor_id = sensor.id) 
        where sensor.id = {}
        LIMIT 1;'''.format(id)
    sensor_data = MysqlConnection().getData(sql=sql)
    dict = json.loads(clearData(sensor_data[0][0]))

    broker = dict['broker']
    username = dict['user']
    password = dict['password']
    port = dict['port']
    topic = dict['topic']
    
    client = connect_mqtt(broker, port, username, password)
    subscribe(client, topic)
    client.loop_forever()

if __name__ == "__main__":
    main()
