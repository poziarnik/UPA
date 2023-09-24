from .. import DataSet
from neo4j import GraphDatabase, Driver
from neo4j.exceptions import ServiceUnavailable
from time import sleep
from shapely.geometry import Point, LineString
from typing import List, Tuple
import requests


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
        #self.original_data
        #self.driver = GraphDatabase.driver("bolt://localhost:7687")
        #connect(self.driver)
#
        #with self.driver.session() as session:
        #    databases = session.run("SHOW DATABASES")
        #    for record in databases:
        #        print(record["name"])
#
        #self.driver.close()
        self.download_original_dataset()
    
    def download_original_dataset(self):
        response = requests.get("https://data.brno.cz/datasets/mestobrno::zast%C3%A1vky-mhd-public-transport-stops.geojson?where=1=1&outSR=%7B%22latestWkid%22%3A3857%2C%22wkid%22%3A102100%7D")
        
        if response.status_code == 200:
            data = response.content
            print(data)
            

    def is_stop_on_route(self, route_coordinates : List[Tuple[int, int]], stop_coordinates : Tuple[int, int]) -> bool: 
        bus_route = LineString(route_coordinates) 
        bus_stop = Point(stop_coordinates[0], stop_coordinates[1])

        if bus_route.intersects(bus_stop):
            return True
        
        return False

