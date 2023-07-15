import os
import pika
import mysql.connector

class MysqlConnection:
    def __init__(self) -> None:
        self.host = os.getenv('MYSQL_HOST')
        self.port = os.getenv('MYSQL_PORT')
        self.user = os.getenv('MYSQL_USER')
        self.password = os.getenv('MYSQL_PASSWORD')
        self.database= os.getenv('MYSQL_DATABASE')

    def getData(self, sql): 
        conn = mysql.connector.connect(host=self.host, port=self.port, user=self.user, password=self.password,
                                   database=self.database)
        cursor = conn.cursor()

        cursor.execute(sql)
        records = cursor.fetchall()
        
        cursor.close()
        conn.close()

        return records
