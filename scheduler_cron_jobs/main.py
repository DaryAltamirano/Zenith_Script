from kubernetes import client, config
from dotenv import load_dotenv

from supports.CronJobsKubernets import CronJobsKubernets
from supports.ConnectionRabbitMQ import ConnectionRabbitMQ
import yaml
import os 

load_dotenv()

def callback(self, method, properties, body):
    if body['action'] == 'new_sensor':
        scheduler()
    elif body['action'] == 'delete_sensor':
        kubert = CronJobsKubernets()
        kubert.deleteCronJob("cron-jobs-" + body['sensor_id'] , "zenith-beta")

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

def scheduler(id):
    import subprocess

    yml = yaml_to_dict("./cron-job_prueba.yaml")

    yml['metadata']['name'] = 'cron-jobs-' + id
    yml['spec']['schedule'] ="*/1 * * * *" 
    yml['spec']['jobTemplate']['spec']['template']['spec']['containers'][0]['name'] = 'cron-jobs-' + id
    yml['spec']['jobTemplate']['spec']['template']['spec']['containers'][0]['image'] = 'busybox'
    yml['spec']['jobTemplate']['spec']['template']['spec']['containers'][0]['command'] = ['echo', 'Este es un CronJob de prueba.']

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
