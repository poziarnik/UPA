from .. import DataSet
from pymongo import MongoClient

HOSTNAME = "localhost"
PORT = 27017
USERNAME = "root"
PASSWORD = "root"

CONNECTION_STRING = f"mongodb://{USERNAME}:{PASSWORD}@{HOSTNAME}:{PORT}"


class MongoDataSet(DataSet):
    def __init__(self) -> None:
        self.client = MongoClient(HOSTNAME, PORT, username=USERNAME, password=PASSWORD)
        print(self.client.list_database_names())
