from influxdb_client import InfluxDBClient

from .. import DataSet


class InfluxDataSet(DataSet):
    def __init__(self) -> None:
        self.client = InfluxDBClient(
            url=f"http://localhost:8086", token="2e46009c-5a2c-11ee-a5a7-00155d21872d"
        )
        print(self.client.ready())
