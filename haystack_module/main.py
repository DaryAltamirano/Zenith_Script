from dotenv import load_dotenv

from supports.InfluxDbConnection import InfluxDbConnection
from supports.ConnectionRabbitMQ import ConnectionRabbitMQ

load_dotenv()


def callback(self, method, properties, body):
    influxdb = InfluxDbConnection().insertData()



def main():
    channel = ConnectionRabbitMQ().channel()
    ConnectionRabbitMQ().basicConsume(channel, callback, None)


if __name__ == "__main__":
    main()
