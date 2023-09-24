from sys import argv

from dataset import (CassandraDataSet, Dataset_T, InfluxDataSet, MongoDataSet,
                     Neo4jDataSet)

DATASETS: dict[str, Dataset_T] = {
    "mongo": MongoDataSet,
    "influx": InfluxDataSet,
    "cassandra": CassandraDataSet,
    "neo4j": Neo4jDataSet,
}

if __name__ == "__main__":
    obj = DATASETS[argv[1]]()
    obj.process_data()
    obj.close()
