echo "Copying common and models"
cp lib/* supervisor/controller/
cp lib/* supervisor/mqtt_influxdb_bridge/
cp devices.csv supervisor/controller/
cp devices.csv supervisor/mqtt_influxdb_bridge/
cp devices.csv supervisor/dashboard/
cp map.csv supervisor/controller/
cp map.csv supervisor/dashboard/
cp map.csv boat/


echo "Supervisor"
cd supervisor/
docker compose down --remove-orphans ; docker image rm controller mqtt_influxdb_bridge ; docker build -t controller ./controller/ ; docker build -t mqtt_influxdb_bridge ./mqtt_influxdb_bridge/ ; docker compose up -d ;
docker inspect mosquitto | grep IPA
