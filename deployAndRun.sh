echo "Copying common and models"
cp -r lib/* supervisor/controller/
cp -r lib/* supervisor/mqtt_influxdb_bridge/
cp -r lib/* floater/
cp devices.csv supervisor/controller/
cp devices.csv supervisor/mqtt_influxdb_bridge/
cp devices.csv supervisor/dashboard/
cp devices.csv boat/
cp devices.csv floater/
cp map.csv supervisor/controller/
cp map.csv supervisor/dashboard/
cp map.csv boat/

# ask to quit
echo "Press any key to continue"
read -n 1 -s

echo "Supervisor"
cd supervisor/
docker compose down --remove-orphans
docker image rm controller mqtt_influxdb_bridge
docker build -t controller ./controller/
docker build -t mqtt_influxdb_bridge ./mqtt_influxdb_bridge/
docker compose up -d

mosquitto_ip_address=$(docker inspect -f '{{range .NetworkSettings.Networks}} {{.IPAddress}} {{end}}' mosquitto | grep -Eo '[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}')
echo "Mosquitto IP: $mosquitto_ip_address"

FLOATER_IP=192.168.3.19
echo "Floater"
#scp -r ./floater/ nap@192.168.3.19:/home/nap/
sshpass -p "openlab" ssh nap@$FLOATER_IP './batman_installation/create_batman_interface.sh wlan0 10.1.1.19 ; sudo route add -net 172.30.0.0 netmask 255.255.0.0 gw 192.168.3.1 ; cd floater/ ; sed -i "s/HOST_BROKER=.*$/HOST_BROKER='$mosquitto_ip_address'/" .env ; source venv/bin/activate ;  python main.py ; ' &





sleep 5
echo "Testing"
docker exec -itd controller python test.py
docker exec -itd mqtt_influxdb_bridge python test.py
