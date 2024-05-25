from common.batman import Batman
from models.Location import Location
from models.Boat import Boat
import time

def main():
    batman = Batman()  # Create an instance of Batman
    boat = Boat("1", "idle", 1, 0, Location('0', 0, 0), [], Location('0', 0, 0), [])

    while True:
        boat.neighbours = batman.get_neighbours()  # Call with the instance
        print(boat.toJSON())
        time.sleep(1)

if __name__ == "__main__":
    main()
