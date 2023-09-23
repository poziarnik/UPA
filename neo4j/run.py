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


uri = "bolt://localhost:7687"

driver = GraphDatabase.driver(uri, connection_timeout=30)
connect(driver)

with driver.session() as session:
    databases = session.run("SHOW DATABASES")
    for record in databases:
        print(record["name"])

driver.close()