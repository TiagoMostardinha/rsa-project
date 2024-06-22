../batman_installation-master/create_batman_interface.sh wlan0 10.1.1.2
sudo ip route add 172.30.0.0/16 via 192.168.2.1
sed -i "s/HOST_BROKER=.*$/HOST_BROKER='$(cat mosquitto.txt)'/" .env
#pip install -r requirements.txt
echo '\nHOST_ID="obu02"' | tee -a .env
#python main.py