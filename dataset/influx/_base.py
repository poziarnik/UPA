import csv
from enum import Enum
from typing import Any

from influxdb_client import InfluxDBClient
from influxdb_client.client.write_api import SYNCHRONOUS

from .. import DataSet, download_data


def get_number(value: Any):
    try:
        return float(value)
    except ValueError:
        return None


class Header(Enum):
    CODE = 3
    NAME = 4
    OWNER = 5
    LAT = 6
    LON = 7
    TIME = 8
    so2_1h = 9
    no2_1h = 10
    co_8h = 11
    pm10_1h = 12
    o3_1h = 13
    pm10_24h = 14
    pm2_5_1h = 15


class InfluxDataSet(DataSet):
    MEASUREMENT = "air_quality"
    BUCKET = "influx-bucket"
    ORG = "influx-org"

    def __init__(self) -> None:
        self.client = InfluxDBClient(
            url="http://localhost:8086", token="2e46009c-5a2c-11ee-a5a7-00155d21872d"
        )

        self.write_api = self.client.write_api(write_options=SYNCHRONOUS)
        self.query_api = self.client.query_api()

        start = "1970-01-01T00:00:00Z"
        stop = "2030-02-01T00:00:00Z"
        self.client.delete_api().delete(
            start,
            stop,
            f'_measurement="{self.MEASUREMENT}"',
            bucket=self.BUCKET,
            org=self.ORG,
        )

    def close(self) -> None:
        self.client.close()

    def process_data(self) -> None:
        data = download_data(
            "https://data.brno.cz/datasets/mestobrno::kvalita-ovzdu%C5%A1%C3%AD-air-quality.csv?"
            "where=1=1&outSR=%7B%22wkid%22%3A4326%7D"
        ).content.decode("utf-8")

        data = csv.reader(data.splitlines(), delimiter=",")
        _ = next(data)

        air_quality = (
            {
                "measurement": self.MEASUREMENT,
                "tags": {
                    "code": row[Header.CODE.value],
                    "name": row[Header.NAME.value],
                    "owner": row[Header.OWNER.value],
                    "lat": float(row[Header.LAT.value]),
                    "lon": float(row[Header.LON.value]),
                },
                "time": row[Header.TIME.value],
                "fields": {
                    Header(index).name: x
                    for index, value in enumerate(row)
                    if index
                    in (
                        Header.so2_1h.value,
                        Header.no2_1h.value,
                        Header.co_8h.value,
                        Header.pm10_1h.value,
                        Header.o3_1h.value,
                        Header.pm10_24h.value,
                        Header.pm2_5_1h.value,
                    )
                    and (x := get_number(value))
                },
            }
            for row in data
        )

        print(next(air_quality))

        self.write_api.write(bucket=self.BUCKET, org=self.ORG, record=air_quality)
