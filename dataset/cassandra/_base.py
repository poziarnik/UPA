from .. import DataSet
from cassandra.cluster import Cluster, Session, NoHostAvailable, DriverException
from time import sleep


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
