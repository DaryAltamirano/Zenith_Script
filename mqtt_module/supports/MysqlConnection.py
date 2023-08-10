import os
import mysql.connector

class MysqlConnection:
    def __init__(self) -> None:
        self.host = os.getenv('MYSQL_HOST', 'db')
        self.port = os.getenv('MYSQL_PORT', '3306')
        self.user = os.getenv('MYSQL_USER', 'root')
        self.password = os.getenv('MYSQL_PASSWORD', 'root')
        self.database = os.getenv('MYSQL_DATABASE', 'zenith')

    def getData(self, sql):
        conn = mysql.connector.connect(host=self.host, port=self.port, user=self.user, password=self.password,
                                       database=self.database)
        cursor = conn.cursor()

        cursor.execute(sql)
        records = cursor.fetchall()

        cursor.close()
        conn.close()

        return records
