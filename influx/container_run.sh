podman container rm -f -i influx_container
podman run -p 9045:8086 --name influx_container -d influx_image:latest \
      -e DOCKER_INFLUXDB_INIT_MODE=setup \
      -e DOCKER_INFLUXDB_INIT_USERNAME=influx-user \
      -e DOCKER_INFLUXDB_INIT_PASSWORD=influx-password \
      -e DOCKER_INFLUXDB_INIT_ORG=influx-org \
      -e DOCKER_INFLUXDB_INIT_BUCKET=influx-bucket \
echo 'Waiting for database initialization before connecting with driver...'
sleep 80 
python3 influx_manager.py