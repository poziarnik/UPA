from time import sleep

from cassandra.cluster import (Cluster, DriverException, NoHostAvailable,
                               Session)

from .. import DataSet


def connect() -> Session:
    while True:
        try:
            return Cluster(["localhost"]).connect()
        except (NoHostAvailable, DriverException):
            print("Waiting for connection...")
        sleep(2)


class CassandraDataSet(DataSet):
    def __init__(self) -> None:
        self.session = connect()
        self.session.shutdown()
