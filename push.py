# python 3.6

import json
import random
import time

from paho.mqtt import client as mqtt_client


broker = 'broker.emqx.io'
port = 1883
topic = "python/mqtt"
# Generate a Client ID with the publish prefix.
client_id = f'publish-{random.randint(0, 1000)}'
# username = 'emqx'
# password = 'public'


def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    # client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


def publish(client):
    msg_count = 1
    while True:
        time.sleep(1)
        temp_aleatorio = round(random.uniform(20, 31), 2)
        rco2_aleatorio = round(random.uniform(1800, 2000), 2)
        humedad_aleatorio = round(random.uniform(30, 100), 2)
        msg = {
            "id": "dd85475c-a5ef-4a15-b00f-206e408528b2",
            "info.aqi": {
                "ts": "2023-08-22T04:44:50Z",
                "data": {
                    "humidity": humedad_aleatorio,
                    "pm10": 7,
                    "pm25": 6,
                    "rco2 (ppm)": rco2_aleatorio,
                    "temp": temp_aleatorio
                }
            }
        }
        result = client.publish(topic,  json.dumps(msg))
        # result: [0, 1]
        status = result[0]
        if status == 0:
            print(f"Send `{msg}` to topic `{topic}`")
        else:
            print(f"Failed to send message to topic {topic}")
        msg_count += 1
        if msg_count > 500:
            break


def run():
    client = connect_mqtt()
    client.loop_start()
    publish(client)
    client.loop_stop()


if __name__ == '__main__':
    run()
