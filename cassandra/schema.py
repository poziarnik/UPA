from cassandra.cluster import Cluster

cluster = Cluster(["localhost"])  # Use your Cassandra cluster's contact points
session = cluster.connect()  # Create a session to interact with Cassandra

print("hi")
#query = "SELECT * FROM keyspace_name.table_name WHERE column_name = %s"
#result = session.execute(query, ('some_value',))
#
#for row in result:
#    print(row)

session.shutdown()
cluster.shutdown()
