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
    
    cadena_decodificada = body.decode('utf-8')
    body = json.loads(cadena_decodificada)
    protocol = body['protocol']
    id = str(body['sensor_id'])

    if body['action'] == 'new_sensor':
        scheduler(id, protocol)

    elif body['action'] == 'update_sensor':
        kubert = CronJobsKubernets()
        kubert.deleteTask(id , "zenith-beta", protocol)
        scheduler(id, protocol)

    elif body['action'] == 'delete_sensor':
        kubert = CronJobsKubernets()
        kubert.deleteTask(id , "zenith-beta", protocol)

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

def setDict(dict_env):
        
    for diccionario in dict_env:
        if diccionario["name"] == "ID_SENSOR":
            diccionario["value"] = id
        if diccionario["name"] == "RABBITMQ_PORT":
            diccionario["value"] = os.getenv('RABBITMQ_PORT')
        if diccionario["name"] == "RABBITMQ_HOST":
            diccionario["value"] = os.getenv('RABBITMQ_HOST')
        if diccionario["name"] == "RABBITMQ_USER":
            diccionario["value"] = os.getenv('RABBITMQ_USER')
        if diccionario["name"] == "RABBITMQ_PASSWORD":
            diccionario["value"] = os.getenv('RABBITMQ_PASSWORD')
        if diccionario["name"] == "RABBITMQ_PUBLISH_QUEUE":
            diccionario["value"] = os.getenv('RABBITMQ_PUBLISH_QUEUE')
        if diccionario["name"] == "RABBITMQ_CONSUMER_QUEUE":
            diccionario["value"] = os.getenv('RABBITMQ_CONSUMER_QUEUE')
        if diccionario["name"] == "MYSQL_HOST":
            diccionario["value"] = os.getenv('MYSQL_HOST', 'db')
        if diccionario["name"] == "MYSQL_PORT":
            diccionario["value"] = os.getenv('MYSQL_PORT', '3306')
        if diccionario["name"] == "MYSQL_USER":
            diccionario["value"] = os.getenv('MYSQL_USER', 'root')
        if diccionario["name"] == "MYSQL_PASSWORD":
            diccionario["value"] = os.getenv('MYSQL_PASSWORD', 'root')
        if diccionario["name"] == "MYSQL_DATABASE":
            diccionario["value"] = os.getenv('MYSQL_DATABASE', 'zenith')
    return dict_env

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
        yml['spec']['jobTemplate']['spec']['template']['spec']['containers'][0]['image'] = imagenes[protocol]
        dict_env = yml['spec']['jobTemplate']['spec']['template']['spec']['containers'][0]['env']
        for diccionario in dict_env:
            if diccionario["name"] == "ID_SENSOR":
                diccionario["value"] = id
       #dict_env = setDict(dict_env)
        yml['spec']['jobTemplate']['spec']['template']['spec']['containers'][0]['env'] = dict_env

        file = './cron_jobs_' + id + '.yaml'
    else: 
        yml = yaml_to_dict("./jobs_prueba.yaml")

        yml['metadata']['name'] = 'jobs-' + id
        yml['spec']['template']['spec']['containers'][0]['name'] = 'jobs-' + id
        yml['spec']['template']['spec']['containers'][0]['image'] = imagenes[protocol]

        dict_env = yml['spec']['template']['spec']['containers'][0]['env']

        for diccionario in dict_env:
            if diccionario["name"] == "ID_SENSOR":
                diccionario["value"] = id
        #dict_env = setDict(dict_env)

        yml['spec']['template']['spec']['containers'][0]['env'] = dict_env

        file = './job_' + id + '.yaml'

    dict_to_yaml_file(yml, file)

    command = "kubectl apply -f " + file
    subprocess.check_output(command, shell=True, text=True)

    os.remove(file)

def main():
    channel = ConnectionRabbitMQ().channel()
    ConnectionRabbitMQ().basicConsume(channel, callback, None)

if __name__ == "__main__":
    main()
