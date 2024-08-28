import os
from urllib.parse import quote_plus
from motor.motor_asyncio import AsyncIOMotorClient

# Use environment variables for sensitive information
MONGO_USERNAME = quote_plus("pavan_tech")
MONGO_PASSWORD = quote_plus("Amma@9502")
MONGO_DBNAME = "pavan"

MONGO_DETAILS = f"mongodb+srv://{MONGO_USERNAME}:{MONGO_PASSWORD}@cluster0.3zqhlo9.mongodb.net/{MONGO_DBNAME}?retryWrites=true&w=majority&appName=Cluster0"

def get_database():
    client = AsyncIOMotorClient(MONGO_DETAILS)
    return client[MONGO_DBNAME]

# Call the function to get the database connection
get_database()