from typing import Protocol
import influxdb_client
from cassandra.cluster import Cluster
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from neo4j import GraphDatabase, RoutingControl


class Db_manager(Protocol):
    def connect(self) -> None:
        ...
    
    def send_data(self) -> None:
        ...
    
class Mongo_manager(Db_manager):
    def connect(self, uri) -> None:
        self.client = MongoClient(uri, server_api=ServerApi('1'))

class Cassandra_manager(Db_manager):
    def connect(self, url) -> None:
        cluster = Cluster(["localhost"])
        self.session = cluster.connect()

class Influx_manager(Db_manager):
    def connect(self, url, token) -> None:
        self.client = influxdb_client.InfluxDBClient(url=url, token=token)
        self.query_api = client.query_api()


class neo4j_manager(Db_manager):
    def connect(self, uri) -> None:
        self.driver = GraphDatabase.driver(uri)

        #with self.driver.session() as session:
        #    databases = session.run("SHOW DATABASES")
        #    for record in databases:
        #        print(record["name"])