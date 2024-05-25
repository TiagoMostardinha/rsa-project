import csv
import json
import subprocess
from csv import reader
from models.Location import Location
from models.Neighbour import Neighbour
from dataclasses import dataclass
import time  

def printNeighbours(neighbours):
    # Use the list of neighbours for further processing or output
            print(f"Neighbours:")
            for neighbour in neighbours:
                print(f"  Neighbor: {neighbour.name}")
                print(f"  Last Seen (ms): {neighbour.last_seen}")
                print(f"  Link Quality: {neighbour.tq}")
                print(f"  Location: {neighbour.location}")  # Assuming location is formatted as a string
                print() 

def get_neighbours(devices):  # Interval parameter

    try:
        command = ["sudo", "batctl", "oj"] 
        completed_process = subprocess.run(command, capture_output=True, text=True)

        if completed_process.returncode == 0:
            # print("Command '{}' executed successfully!".format(" ".join(command)))

            json_string = completed_process.stdout.strip()
            data = json.loads(json_string)  # Assuming the JSON structure aligns with Neighbour

            neighbours = [
                Neighbour(
                    name=devices.get(network["neigh_address"], network["neigh_address"]),
                    tq=network["tq"],
                    location=Location.get_location(network["neigh_address"]),  # Assuming location retrieval logic
                    last_seen=network["last_seen_msecs"]
                )
                for network in data
            ]

            return neighbours

        else:
            print("Command '{}' failed with return code: {}".format(" ".join(command), completed_process.returncode))

    except (ValueError, RuntimeError) as e:
        print(f"Error: {e}")

    # Sleep for the specified interval before the next retrieval

def main():
    # Load the devices map from a CSV file
    devices = {}
    filename = "devices_map.csv"

    try:
        with open(filename, 'r') as csvfile:
            for row in reader(csvfile):  # Using csv.reader directly
                if len(row) == 2:
                    mac_address, device_name = row
                    devices[mac_address] = device_name
    except FileNotFoundError:
        print(f"Error: Could not find devices map file '{filename}'.")
    except csv.Error as e:
        print(f"Error: Error parsing devices map file '{filename}': {e}")

    # Call get_neighbours with an optional interval (e.g., 10 seconds)
    while True:
        neighbours =  get_neighbours(devices)
        printNeighbours(neighbours)
        time.sleep(1)


if __name__ == "__main__":
    main()
