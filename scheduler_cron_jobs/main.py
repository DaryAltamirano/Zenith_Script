from kubernetes import client, config
from dotenv import load_dotenv

from supports.ConnectionRabbitMQ import ConnectionRabbitMQ

load_dotenv()


def callback(self, method, properties, body):
    print("hola")


def main():
    channel = ConnectionRabbitMQ().channel()
    ConnectionRabbitMQ().basicConsume(channel, callback, None)


if __name__ == "__main__":
    main()
