from boat.pub.common.batman import Batman
from models import Location
from supervisor.controller.models.Boat import Boat
import time

def main():
    batman = Batman()
    boat = Boat("1", "idle", 1, 0, Location('0', 0, 0), [], Location('0', 0, 0), [])

    while True:
        boat.neighbours = batman.get_neighbours()
        print(boat.toJSON())
        time.sleep(1)
        
        
