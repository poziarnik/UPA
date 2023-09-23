from .. import DataSet
from neo4j import GraphDatabase, Driver
from neo4j.exceptions import ServiceUnavailable
from time import sleep


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

        self.driver.close()
