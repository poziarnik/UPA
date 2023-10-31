import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS


url = "http://localhost:9045"
token = "influx-password",
org="influx-org"
client = influxdb_client.InfluxDBClient(url=url, token=token)

query_api = client.query_api()

# Use the query API to execute a query to list databases
query = 'buckets() |> keys()'
databases = query_api.query(query=query)

# Print the list of databases
for database in databases:
    print(database)