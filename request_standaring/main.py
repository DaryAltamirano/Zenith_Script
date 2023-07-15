import os
from dotenv import load_dotenv
import time
from supports.ConnectionRabbitMQ import ConnectionRabbitMQ

load_dotenv()

def callback(self, method, properties, body):
        print(" [x] Received %r" % body)

def main():
    print("Hello, world!")
    channel = ConnectionRabbitMQ().channel()
    ConnectionRabbitMQ().basicConsume(channel, callback, None)

    # Rest of your code goes here


if __name__ == "__main__":
    main()
