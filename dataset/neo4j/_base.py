from time import sleep

from haversine import Unit, haversine
from neo4j import Driver, GraphDatabase
from neo4j.exceptions import ServiceUnavailable
from tqdm import tqdm

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

        self.driver.execute_query("Match (n) DETACH DELETE n")

    def __add_stop(
        self, stop_name: str, stop_index: int, vehicle_name: str, vehicle_id: str
    ) -> None:
        self.driver.execute_query(
            "MERGE (s:Stop {name: $stop_name}) "
            "MERGE (v:Vehicle {name: $vehicle_name, id: $vehicle_id}) "
            "MERGE (v)-[:STOPS {index: $stop_index}]->(s)",
            stop_name=stop_name,
            stop_index=stop_index,
            vehicle_name=vehicle_name,
            vehicle_id=vehicle_id,
        )

    def close(self) -> None:
        self.driver.close()

    def process_data(self) -> None:
        # self.__add_stop("Cervinkova", 0, "12", 1)
        # self.__add_stop("Skacelova", 1, "12", 1)
        # self.__add_stop("Cervinkova", 1, "12", 0)
        # self.__add_stop("Skacelova", 0, "12", 0)
        # self.__add_stop("Skacelova", 0, "44", 5)

        # download public transport stops and routes
        mhd_stops = download_geojson(
            "https://data.brno.cz/datasets/mestobrno::zast%C3%A1vky-mhd-public-transport-stops.geojson?where=1=1&outSR=%7B%22latestWkid%22%3A3857%2C%22wkid%22%3A102100%7D"
        )

        mhd_routes = download_geojson(
            "https://data.brno.cz/datasets/mestobrno::veden%C3%AD-linek-mhd-public-transit-routes.geojson?where=1=1&outSR=%7B%22latestWkid%22%3A3857%2C%22wkid%22%3A102100%7D"
        )

        # loop through transport routes
        for vehicle_id, vehicle_name, route_coord in tqdm(
            find_in_json_object(
                mhd_routes["features"],
                "properties.ID",
                "properties.naz_linky",
                "geometry.coordinates",
            )
        ):
            index = 0
            stops = set()
            for stop_name, stop_coord in find_in_json_object(
                mhd_stops["features"], "properties.stop_name", "geometry.coordinates"
            ):
                for coord in route_coord[0]:
                    if (stop_name not in stops) and haversine(
                        coord, stop_coord, Unit.METERS
                    ) <= 10:
                        stops.add(stop_name)
                        self.__add_stop(stop_name, index, vehicle_name, vehicle_id)
                        index += 1
