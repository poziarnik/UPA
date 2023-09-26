from pymongo import MongoClient
from .. import DataSet, download_data
import csv
from io import StringIO

HOSTNAME = "localhost"
PORT = 27017
USERNAME = "root"
PASSWORD = "root"

CONNECTION_STRING = f"mongodb://{USERNAME}:{PASSWORD}@{HOSTNAME}:{PORT}"


class MongoDataSet(DataSet):
    def __init__(self) -> None:
        self.client = MongoClient(HOSTNAME, PORT, username=USERNAME, password=PASSWORD)
        self.db = self.client["default"]
        self.db.get_collection("bin").delete_many({})

    def close(self) -> None:
        self.client.close()

    def process_data(self) -> None:
        bin_collection = self.db.create_collection("bin")

        content = download_data(
            "https://data.brno.cz/datasets/mestobrno::odpadkov%C3%A9-ko%C5%A1e-litter-bins.csv?where=1=1&outSR=%7B%22latestWkid%22%3A3857%2C%22wkid%22%3A102100%7D"
        ).text

        reader = csv.reader(StringIO(content), delimiter=",")
        header = next(reader)

        bin_data = (
            {key: row[index] for index, key in enumerate(header) if row[index]}
            for row in reader
        )

        bin_collection.insert_many(bin_data)
