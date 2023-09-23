podman container rm -f -i cassandra_container
podman run -p 9042:9042 --name cassandra_container -d cassandra_image:latest 
echo 'Waiting for database initialization befor connecting with driver...'
sleep 80 #treba pockat na inicializaciu databazy pred pripojenim
python3 schema.py