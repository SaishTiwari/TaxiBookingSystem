import mysql.connector
from mysql.connector import Error

def create_connection():

    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='pcps@123',
            database='TaxiBookingSystem'
        )
        if connection.is_connected():
            print("Connection to the database established successfully.")
            return connection
    except Error as e:
        print(f"Error while connecting to the database: {e}")
        return None

def close_connection(connection):

    if connection and connection.is_connected():
        connection.close()
        print("Database connection closed.")