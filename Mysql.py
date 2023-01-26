import mysql.connector
from mysql.connector import Error

from Log import Log

class Mysql:

    connection = None

    @staticmethod
    def getConnection():
        if Mysql.connection == None:
            logins = open('../database-login.txt', 'r').readlines()[0].split(';')
            Mysql.connection = create_connection(logins[0], logins[1], logins[2], logins[3])
            if Mysql.connection is None:
                Log.print("Connection failed")
                raise Exception("Connection failed")
        return Mysql.connection

    @staticmethod
    def create_connection(host_name, user_name, user_password, db_name):
        connection = None
        try:
            connection = mysql.connector.connect(
                host=host_name,
                user=user_name,
                passwd=user_password,
                database=db_name
            )
            Log.print("Connection to MySQL DB successful")
        except Error as e:
            Log.print(f"The error '{e}' occurred")
        return connection

    def execute_query(self, query):
        connection = Mysql.getConnection()
        cursor = connection.cursor()
        try:
            cursor.execute(query)
            connection.commit()
            Log.print("Query executed successfully")
        except Error as e:
            Log.print(f"The error '{e}' occurred")

    def execute_read_query(self, query):
        connection = Mysql.getConnection()
        cursor = connection.cursor()
        result = None
        try:
            cursor.execute(query)
            result = cursor.fetchall()
            return result
        except Error as e:
            Log.print(f"The error '{e}' occurred")

    @staticmethod
    def injection_protection(string):
        return string.replace("'", "\\'")

    @staticmethod
    def remove_injection_protection(string):
        return string.replace("\\'", "'")