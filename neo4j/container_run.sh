podman container rm -f -i neo4j_container
podman run -p 9044:7687 --env=NEO4J_AUTH=none --name neo4j_container -d neo4j_image:latest 
echo 'Waiting for database initialization before connecting with driver...'
sleep 80 
python3 schema.py