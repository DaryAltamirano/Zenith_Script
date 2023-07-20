import os
from dotenv import load_dotenv
import time

from supports.MysqlConnection import MysqlConnection
from supports.ConnectionRabbitMQ import ConnectionRabbitMQ

load_dotenv()

def callback(self, method, properties, body):
    id = os.getenv('ID_SENSOR')

    sql = '''select format
                from sensor_driver_sensor  
                where id = {}
                LIMIT 1;'''.format(id)

    sensor_data = MysqlConnection().getData(sql=sql)
    print(sensor_data)
def main():
    channel = ConnectionRabbitMQ().channel()
    ConnectionRabbitMQ().basicConsume(channel, callback, None)


if __name__ == "__main__":
    main()
