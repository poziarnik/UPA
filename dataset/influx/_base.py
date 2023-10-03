from typing import Any, Callable

from influxdb_client import InfluxDBClient
from influxdb_client.client.write_api import SYNCHRONOUS

from .. import DataSet, download_geojson


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
        data = download_geojson(
            "https://data.brno.cz/datasets/mestobrno::kvalita-ovzdu%C5%A1%C3%AD-air-quality.geojson?"
            "where=1=1&outSR=%7B%22wkid%22%3A4326%7D"
        )

        get_values: Callable[
            [dict[str, Any], list[str]], dict[str, Any]
        ] = lambda row, keys: {key: row[key] for key in keys if row[key] != "null"}

        air_quality = (
            {
                "measurement": self.MEASUREMENT,
                "tags": get_values(
                    row["properties"], ["code", "name", "owner", "lat", "lon"]
                ),
                "time": get_values(row["properties"], ["actualized"])["actualized"],
                "fields": get_values(
                    row["properties"],
                    [
                        "so2_1h",
                        "no2_1h",
                        "co_8h",
                        "pm10_1h",
                        "o3_1h",
                        "pm10_24h",
                        "pm2_5_1h",
                    ],
                ),
            }
            for row in data["features"]
        )

        self.write_api.write(bucket=self.BUCKET, org=self.ORG, record=air_quality)

    def request_data(self) -> Any:
        q = """
            from(bucket: influx-bucket)
            |> range(start: -5m, stop: now())
        """

        tables = self.query_api.query(query=q)

        return {table: [row for row in table] for table in tables}
