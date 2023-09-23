podman container rm -f -i mongo_container
podman run -p 9043:27017 --name mongo_container -d mongo_image:latest 
echo 'Waiting for database initialization before connecting with driver...'
#sleep 80 
python3 schema.py