docker run -d -p 8086:8086 --name influxdb2 \
    -v $PWD/data:/var/lib/influxdb2 \
    -v $PWD/config:/etc/influxdb2 \
    -e DOCKER_INFLUXDB_INIT_MODE=setup \
    -e DOCKER_INFLUXDB_INIT_USERNAME=mayank \
    -e DOCKER_INFLUXDB_INIT_PASSWORD=password123 \
    -e DOCKER_INFLUXDB_INIT_ORG=tokopedia \
    -e DOCKER_INFLUXDB_INIT_BUCKET=ml_app \
    influxdb:2.0