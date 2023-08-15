from kubernetes import client, config
from dotenv import load_dotenv

from supports.CronJobsKubernets import CronJobsKubernets
from supports.ConnectionRabbitMQ import ConnectionRabbitMQ
from supports.MysqlConnection import MysqlConnection
from supports.ConnectionRabbitMQ import ConnectionRabbitMQ
import yaml
import os 
import json

load_dotenv()

def callback(self, method, properties, body):

    sql = '''select sensor.protocol
        from sensor_driver_sensor as sensor
        inner join sensor_driver_request as request on (request.sensor_id = sensor.id) 
        inner join sensor_driver_scheduler as scheduler on (scheduler.sensor_id = sensor.id) 
        where sensor.id = {}
        LIMIT 1;'''.format(id)
    sensor_data = MysqlConnection().getData(sql=sql)

    protocol = sensor_data[0][0]
    
    if body['action'] == 'new_sensor':
        scheduler(body['sensor_id'], protocol)

    elif body['action'] == 'update_sensor':
        kubert = CronJobsKubernets()
        kubert.deleteCronJob("cron-jobs-" + body['sensor_id'] , "zenith-beta", protocol)
        scheduler(body['sensor_id'], protocol)

    elif body['action'] == 'delete_sensor':
        kubert = CronJobsKubernets()
        kubert.deleteCronJob("cron-jobs-" + body['sensor_id'] , "zenith-beta", protocol)

def clearData(sensor_data):
    string = sensor_data.replace("\'", "\"").replace("\\", "")
    return string[1: len(string) - 1]

def yaml_to_dict(yaml_path):
    # Carga el contenido del archivo YAML
    with open(yaml_path, 'r') as yaml_file:
        yaml_content = yaml_file.read()

    # Convierte el contenido YAML en un objeto Python
    yaml_data = yaml.safe_load(yaml_content)

    return yaml_data

def dict_to_yaml_file(data, file_path):
    with open(file_path, 'w') as yaml_file:
        yaml.dump(data, yaml_file, default_flow_style=False)

def scheduler(id, protocol):
    import subprocess
    crons = ["http", "coap"]
    imagenes = {
        "http": "darypte/http-zenith:latest",
        "coap": "darypte/coap-zenith:latest",
        "mqtt": "darypte/mqtt-zenith:latest",
        "modbus": "darypte/modbus-zenith:latest"
    }
    if protocol in crons:
        yml = yaml_to_dict("./cron-job_prueba.yaml")

        yml['metadata']['name'] = 'cron-jobs-' + id
        yml['spec']['schedule'] ="*/1 * * * *" 
        yml['spec']['jobTemplate']['spec']['template']['spec']['containers'][0]['name'] = 'cron-jobs-' + id
        yml['spec']['jobTemplate']['spec']['template']['spec']['containers'][0]['image'] = imagenes['protocol']

        file = './cron_jobs_' + id + '.yaml'
        
    dict_to_yaml_file(yml, file)

    command = "kubectl apply -f " + file
    subprocess.check_output(command, shell=True, text=True)

    os.remove(file)

def main():
    channel = ConnectionRabbitMQ().channel()
    ConnectionRabbitMQ().basicConsume(channel, callback, None)

if __name__ == "__main__":
    main()
