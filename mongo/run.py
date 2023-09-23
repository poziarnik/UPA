from pymongo import MongoClient

HOSTNAME = "localhost"
PORT = 27017
USERNAME = "root"
PASSWORD = "root"

CONNECTION_STRING = f"mongodb://{USERNAME}:{PASSWORD}@{HOSTNAME}:{PORT}"

client = MongoClient(HOSTNAME, PORT, username=USERNAME, password=PASSWORD)
print(client.list_database_names())
