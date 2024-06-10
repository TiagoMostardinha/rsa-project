echo "Copying common and models"
cp -r lib/* supervisor/controller/
cp -r lib/* supervisor/mqtt_influxdb_bridge/
cp -r lib/* floater/
cp -r lib/* boat/
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

# echo "Supervisor"
# cd supervisor/
# docker compose down --remove-orphans
# docker image rm controller mqtt_influxdb_bridge
# docker build -t controller ./controller/
# docker build -t mqtt_influxdb_bridge ./mqtt_influxdb_bridge/
# docker compose up -d
# cd ..

mosquitto_ip_address=$(docker inspect -f '{{range .NetworkSettings.Networks}} {{.IPAddress}} {{end}}' mosquitto | grep -Eo '[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}')
echo "Mosquitto IP: $mosquitto_ip_address"
echo $mosquitto_ip_address > boat/mosquitto.txt

sleep 5

sudo route add -net 0.0.0.0 netmask 0.0.0.0 gw 192.168.2.2
sudo route add -net 0.0.0.0 netmask 0.0.0.0 gw 192.168.19.19

# FLOATER_IP=192.168.19.19
# echo "Floater"
# #scp -r ./floater/ nap@192.168.19.19:/home/nap/

BOAT1_IP=192.168.19.19
echo "BOAT1"
sshpass -p "openlab" scp -r boat/ nap@192.168.19.19:/home/nap
#sshpass -p "openlab" ssh nap@$BOAT1_IP "cd /home/nap/boat ; source venv/bin/activate ; sh boat10.sh " &

BOAT2_IP=192.168.2.2
echo "BOAT2"
sshpass -p "openlab" scp -r boat/ nap@192.168.2.2:/home/nap
#sshpass -p "openlab" ssh nap@$BOAT2_IP "cd /home/nap/boat ; source venv/bin/activate ; sh boat02.sh " &

# sleep 5
# echo "Testing"
# docker exec -itd controller python test.py
# docker exec -itd mqtt_influxdb_bridge python test.py
