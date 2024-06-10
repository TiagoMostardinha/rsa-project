../batman_installation-master/create_batman_interface.sh wlan0 10.1.1.19
sudo route add -net 172.30.0.0 netmask 255.255.0.0 gw 192.168.19.1
sudo route add -net 0.0.0.0 netmask 0.0.0.0 gw 192.168.19.1
sed -i "s/HOST_BROKER=.*$/HOST_BROKER='$(cat mosquitto.txt)'/" .env
#pip install -r requirements.txt
echo '\nHOST_ID="obu19"' | tee -a .env
#python main.py