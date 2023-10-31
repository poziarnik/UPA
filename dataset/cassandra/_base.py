from time import sleep

from cassandra.cluster import (Cluster, DriverException, NoHostAvailable,
                               Session)

from .. import DataSet, download_json, find_in_json_object
import uuid


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
        
        self.processData()

        print("hi")
        self.session.shutdown()

        

    def processData(self):

        keyspace_name = 'traffic_accidents'
        replication_strategy = 'SimpleStrategy'  # Or 'NetworkTopologyStrategy' for more complex setups
        replication_options = {'replication_factor': 3}  # Adjust the replication factor as needed

        # Create the keyspace
        create_keyspace_query = f"""
        CREATE KEYSPACE IF NOT EXISTS {keyspace_name}
        WITH replication = {{
            'class': '{replication_strategy}',
            {', '.join([f"'{key}': {value}" for key, value in replication_options.items()])}
        }}
        """
        self.session.execute(create_keyspace_query)
        
        self.session.set_keyspace("traffic_accidents")

        drop_table_query = f"DROP TABLE IF EXISTS accidents;"
        self.session.execute(drop_table_query)
        
        create_table_query = """
        CREATE TABLE IF NOT EXISTS accidents (
            accident_id UUID,
            datum TIMESTAMP,
            zavineni TEXT,
            viditelnost TEXT,
            situovani TEXT,
            alkohol TEXT,
            alkohol_vinik TEXT,
            nasledky TEXT,
            pricina TEXT,
            smrt BIGINT,
            PRIMARY KEY(smrt, alkohol)
        )
        """
        self.session.execute(create_table_query)

        
        traffic_accidents = download_json(
            "https://opendata.arcgis.com/api/v3/datasets/298c37feb1064873abdccdc2a10b605f_0/downloads/data?format=geojson&spatialRefId=4326&where=1%3D1"
        )

        insert_data_query = """
        INSERT INTO accidents (accident_id, datum, zavineni, viditelnost, situovani, alkohol, alkohol_vinik, nasledky, pricina, smrt)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
        """

        for accident in find_in_json_object(
                traffic_accidents["features"], "properties.datum", "properties.zavineni", "properties.viditelnost", "properties.situovani",
                  "properties.alkohol", "properties.alkohol_vinik", "properties.nasledky", "properties.pricina", "properties.smrt"
            ):
            self.session.execute(insert_data_query, (uuid.uuid1(), accident[0], accident[1], accident[2], accident[3], accident[4], accident[5], accident[6], accident[7], int(accident[8])))

        #self.session.set_keyspace('traffic_accidents')




        
