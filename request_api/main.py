import os
from dotenv import load_dotenv
import time
from supports.MysqlConnection import MysqlConnection
from supports.ConnectionRabbitMQ import ConnectionRabbitMQ

load_dotenv()


def main():

    print(os.getenv('UUID_SENSOR'))
    sql = "SELECT * FROM TABLES WHERE TABLE_SCHEMA LIKE 'information_schema';"
    sensor_data = MysqlConnection().getData(sql=sql)

    print(sensor_data)


if __name__ == "__main__":
    main()
