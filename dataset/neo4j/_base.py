from operator import itemgetter
from pprint import pprint
from time import sleep

import pandas as pd
import requests
from neo4j import Driver, GraphDatabase
from neo4j.exceptions import ServiceUnavailable

from .. import DataSet


def connect(driver: Driver):
    while True:
        try:
            with driver.session() as session:
                session.run("Match () Return 1 Limit 1")
                return True
        except ServiceUnavailable:
            print("Waiting for connection...")

        sleep(2)


class Neo4jDataSet(DataSet):
    def __init__(self) -> None:
        self.driver = GraphDatabase.driver("bolt://localhost:7687")
        connect(self.driver)

        with self.driver.session() as session:
            databases = session.run("SHOW DATABASES")
            for record in databases:
                print(record["name"])

    def close(self) -> None:
        self.driver.close()

    def process_data(self) -> None:
        # download MHD stops in geojson format
        response = requests.get(
            "https://data.brno.cz/datasets/mestobrno::zast%C3%A1vky-mhd-public-transport-stops.geojson?where=1=1&outSR=%7B%22latestWkid%22%3A3857%2C%22wkid%22%3A102100%7D"
        )

        if response.status_code != 200:
            raise RuntimeError("Unable to download data!")

        # columns names from the dataset
        columns = ("stop_name", "latitude", "longitude")

        data = (
            itemgetter(*columns)(feature["properties"])
            for feature in response.json()["features"]
        )

        mhd_stops = pd.DataFrame(data, columns=columns)
        pprint(mhd_stops)
