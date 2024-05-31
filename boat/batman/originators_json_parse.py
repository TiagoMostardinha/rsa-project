import json
import subprocess
from csv import reader


class WifiNetwork:
    """
    Represents a Wi-Fi network as parsed from the `batctl oj` command output.

    Attributes:
        orig_address (str): The original MAC address associated with the network.
        best (bool): Whether this is the best available network (True) or not.
        last_seen_msecs (int): The time in milliseconds since the network was last seen.
        neigh_address (str): The neighbor's MAC address (or potentially a device name).
        tq (int): The link quality (higher is better).
    """

    def __init__(self, data):
        """
        Initializes a WifiNetwork instance from a dictionary.

        Args:
            data (dict): A dictionary containing the parsed JSON data.
        """

        self.last_seen_msecs = data["last_seen_msecs"]
        self.neigh_address = data["neigh_address"]
        self.tq = data["tq"]

    @classmethod
    def from_json(cls, json_string):
        """
        Parses a JSON string representing the `batctl oj` output and returns a list of WifiNetwork instances.

        Args:
            json_string (str): The JSON string to parse.

        Returns:
            list: A list of WifiNetwork instances.
        """

        try:
            data = json.loads(json_string)
            if not isinstance(data, list):
                raise ValueError("Expected a list of network data")
            return [cls(network) for network in data]
        except (json.JSONDecodeError, ValueError) as e:
            raise ValueError(f"Invalid JSON data: {e}")


def load_devices_map(filename):
    """
    Loads a device mapping from a CSV file.

    Args:
        filename (str): The path to the CSV file.

    Returns:
        dict: A dictionary mapping MAC addresses to device names.
    """

    devices = {}
    try:
        with open(filename, 'r') as csvfile:
            for row in reader(csvfile):  # Using csv.reader directly
                # Handle rows with missing data gracefully
                if len(row) == 2:
                    mac_address, device_name = row
                    devices[mac_address] = device_name
            
    except FileNotFoundError:
        print(f"Error: Could not find devices map file '{filename}'.")
    except csv.Error as e:
        print(f"Error: Error parsing devices map file '{filename}': {e}")

    return devices


def main():
    """
    Parses the JSON output from `sudo batctl oj`, processes devices map, and substitutes MAC addresses.
    """

    devices = load_devices_map("devices.csv")  # Replace with your CSV file path

    try:
        command = ["sudo", "batctl", "oj"]  # Use "oj" for JSON output
        completed_process = subprocess.run(command, capture_output=True, text=True)

        if completed_process.returncode == 0:
        #    print("Command '{}' executed successfully!".format(" ".join(command)))

            json_string = completed_process.stdout.strip()
            networks = WifiNetwork.from_json(json_string)
            for network in networks:
                # Substitute MAC address with device name from the map (if found)
                device_name = devices.get(network.neigh_address)
                if device_name:
                    network.neigh_address = device_name
                print(f"  Neighbor: {network.neigh_address}")
                print(f"  Last Seen (ms): {network.last_seen_msecs}")
                print(f"  Link Quality: {network.tq}")
              
        else:
            print("Command '{}' failed with return code: {}".format(" ".join(command), completed_process.returncode))

    except ValueError as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()

