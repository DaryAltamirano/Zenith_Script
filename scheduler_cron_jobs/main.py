from kubernetes import client, config
from dotenv import load_dotenv

from supports.CronJobsKubernets import CronJobsKubernets
from supports.ConnectionRabbitMQ import ConnectionRabbitMQ

load_dotenv()


def callback(self, method, properties, body):
    print("hola")


def main():
    config.load_kube_config()

    prueba = CronJobsKubernets()
    prueba.create_cronjob("prueba", "zenith")
    # print(v1.delete_namespaced_cron_job(name="test-cronjob", namespace="zenith"))


    # channel = ConnectionRabbitMQ().channel()
    # ConnectionRabbitMQ().basicConsume(channel, callback, None)


if __name__ == "__main__":
    main()
