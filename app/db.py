import os
from urllib.parse import quote_plus
from motor.motor_asyncio import AsyncIOMotorClient
import mysql.connector
from mysql.connector import Error
# Use environment variables for sensitive information
MONGO_USERNAME = quote_plus("pavan_tech")
MONGO_PASSWORD = quote_plus("Amma@9502")
MONGO_DBNAME = "pavan"

MONGO_DETAILS = f"mongodb+srv://{MONGO_USERNAME}:{MONGO_PASSWORD}@cluster0.3zqhlo9.mongodb.net/{MONGO_DBNAME}?retryWrites=true&w=majority&appName=Cluster0"

def get_database():
    client = AsyncIOMotorClient(MONGO_DETAILS)
    return client[MONGO_DBNAME]


def get_db():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',  # replace with your MySQL username
            password='Amma@9502',  # replace with your MySQL password
            database='pavan'  # replace with your MySQL database name
        )
        if connection.is_connected():
            print("Connected to MySQL database")
            return connection
    except Error as e:
        print(f"Error while connecting to MySQL: {e}")
        return None
