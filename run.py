from sys import argv
from dataset import (
    MongoDataSet,
    InfluxDataSet,
    CassandraDataSet,
    Neo4jDataSet,
    Dataset_T,
)


DATASETS: dict[str, Dataset_T] = {
    "mongo": MongoDataSet,
    "influx": InfluxDataSet,
    "cassandra": CassandraDataSet,
    "neo4j": Neo4jDataSet,
}

if __name__ == "__main__":
    obj = DATASETS[argv[1]]()
