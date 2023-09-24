from operator import itemgetter
from pprint import pprint
from time import sleep
from typing import Any, Iterator

import pandas as pd
from haversine import haversine
from neo4j import Driver, GraphDatabase
from neo4j.exceptions import ServiceUnavailable

from .. import DataSet, download_geojson, find_in_json_object


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

        self.__run_cypher_query("Match (n)\nDETACH DELETE n")

    def __run_cypher_query(
        self, query: str, parameters: dict[str, Any] | None = None
    ) -> None:
        with self.driver.session() as session:
            session.run(query, parameters)

    def close(self) -> None:
        self.driver.close()

    def process_data(self) -> None:
        # download public transport stops and routes
        mhd_stops = download_geojson(
            "https://data.brno.cz/datasets/mestobrno::zast%C3%A1vky-mhd-public-transport-stops.geojson?where=1=1&outSR=%7B%22latestWkid%22%3A3857%2C%22wkid%22%3A102100%7D"
        )

        mhd_routes = download_geojson(
            "https://data.brno.cz/datasets/mestobrno::veden%C3%AD-linek-mhd-public-transit-routes.geojson?where=1=1&outSR=%7B%22latestWkid%22%3A3857%2C%22wkid%22%3A102100%7D"
        )

        # create stop entities
        stop_entities = [
            f"(s:Stop {{name:'{ result[0] }'}})"
            for result in find_in_json_object(
                mhd_stops, "features[*].properties.stop_name"
            )
        ]

        create_stop_query = f"CREATE\n\t" + ",\n\t".join(stop_entities)
        self.__run_cypher_query(create_stop_query)

        # create vehicle entities
        vehicle_entities = [
            f"(v:Vehicle {{name:'{ result[1] }-{ result[0] }', type:'{ result[2] }'}})"
            for result in find_in_json_object(
                mhd_routes["features"],
                *[f"properties.{key}" for key in ("ID", "naz_linky", "typ")],
            )
        ]

        create_vehicle_query = f"CREATE\n\t" + ",\n\t".join(vehicle_entities)
        print(create_vehicle_query)
        self.__run_cypher_query(create_vehicle_query)

        # def data_generator() -> Iterator[tuple]:
        #     # column names from the stops
        #     stop_columns = ("stop_name", "latitude", "longitude")

        #     # column names from the routes
        #     route_columns = ("naz_linky", "typ")

        #     for route_point in mhd_routes["features"]["properties"]["geometry"]["coordinates"][0]:
        #         stops = []
        #         for stop in mhd_stops
        #             if haversine(route_point, (stop["latitude"], stop["longitude"])) < 0.02: # 20m
        #                 stops

        # data = (
        #     itemgetter(*stop_columns)(feature["properties"])
        #     for feature in mhd_stops["features"]
        # )

        # mhd_dataframe = pd.DataFrame(data, columns=stop_columns)
        # pprint(mhd_dataframe)
