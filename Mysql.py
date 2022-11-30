import mysql.connector
from mysql.connector import Error

from Log import Log

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

def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        Log.print("Query executed successfully")
    except Error as e:
        Log.print(f"The error '{e}' occurred")

def execute_read_query(connection, query):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as e:
        Log.print(f"The error '{e}' occurred")

def injection_protection(string):
    return string.replace("'", "\\'")

def remove_injection_protection(string):
    return string.replace("\\'", "'")