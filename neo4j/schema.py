from neo4j import GraphDatabase, RoutingControl

uri = "bolt://localhost:9044"

driver = GraphDatabase.driver(uri)

with driver.session() as session:
    databases = session.run("SHOW DATABASES")
    for record in databases:
        print(record["name"])

driver.close()