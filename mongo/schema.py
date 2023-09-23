from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

uri = "mongodb://localhost:9043"
client = MongoClient(uri, server_api=ServerApi('1'))

database_names = client.list_database_names()


print(database_names)