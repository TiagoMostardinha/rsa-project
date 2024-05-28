import subprocess
import json
import csv
import time
from models.Neighbour import Neighbour
from models.Location import Location

class Batman():

    def get_devices_map(self):
        # Load the devices map from a CSV file
        devices = {}
        filename = "devices_map.csv"

        try:
            with open(filename, 'r') as csvfile:
                for row in csv.reader(csvfile):  # Using csv.reader directly
                    if len(row) == 2:
                        mac_address, device_name = row
                        devices[mac_address] = device_name
        except FileNotFoundError:
            print(f"Error: Could not find devices map file '{filename}'.")
        except csv.Error as e:
            print(f"Error: Error parsing devices map file '{filename}': {e}")
            
        return devices

    def printNeighbours(self, neighbours):
        print(f"Neighbours:")
        for neighbour in neighbours:
            print(f"  Neighbor: {neighbour.name}")
            print(f"  Last Seen (ms): {neighbour.last_seen}")
            print(f"  Link Quality: {neighbour.tq}")
            print(f"  Location: {neighbour.location}")  # Assuming location is formatted as a string
            print() 


    def get_neighbours(self):
        devices = self.get_devices_map()
        try:
            command = ["sudo", "batctl", "oj"]
            completed_process = subprocess.run(command, capture_output=True, text=True)

            if completed_process.returncode == 0:
                json_string = completed_process.stdout.strip()
                data = json.loads(json_string)  # Assuming the JSON structure aligns with Neighbour
                #print(data)
                neighbours = [
                    Neighbour(
                        name=devices.get(network["neigh_address"], network["neigh_address"]),
                        tq=network["tq"],
                        location=Location(id='0', x=0, y=0),  # Use location from JSON if available, otherwise default
                        last_seen=network["last_seen_msecs"]
                    )
                    for network in data
                ]

                return neighbours

            else:
                print("Command '{}' failed with return code: {}".format(" ".join(command), completed_process.returncode))

        except (ValueError, RuntimeError) as e:
            print(f"Error: {e}")
            