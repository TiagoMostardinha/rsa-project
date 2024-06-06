from models.Location import Location
from models.Neighbour import Neighbour


class Boat:
    id: str
    mac: str
    status: str
    speed: int
    direction: int
    location: Location
    destination: Location
    neighbours: list
    transfered_files: list[str]

    def __init__(self, id,mac, status, speed, direction, location, neighbours, destination, transfered_files):
        self.id = id
        self.mac = mac
        self.status = status
        self.speed = speed
        self.direction = direction
        self.location = location
        self.destination = destination
        self.neighbours = neighbours
        self.transfered_files = transfered_files

    def toJSON(self) -> dict:
        return {
            "id": self.id,
            "mac": self.mac,
            "status": self.status,
            "speed": self.speed,
            "direction": self.direction,
            "location": {
                "id": self.location.id,
                "x": self.location.x,
                "y": self.location.y
            } if self.location else "",
            "destination": {
                "id": self.destination.id,
                "x": self.destination.x,
                "y": self.destination.y
            }if self.destination else "",
            "neighbours": [
                {
                    "name": n.name,
                    "mac": n.mac,
                    "tq": n.tq,
                    "location": {
                        "id": n.location.id,
                        "x": n.location.x,
                        "y": n.location.y
                    },
                    "last_seen": n.last_seen
                } for n in self.neighbours
            ],
            "transfered_files": [
                f for f in self.transfered_files
            ] 
        }

    def fromJSON(message):
        return Boat(
            id=message["id"],
            mac=message["mac"],
            status=message["status"],
            speed=message["speed"],
            direction=message["direction"],
            location=Location(
                id=message["location"]["id"],
                x=message["location"]["x"],
                y=message["location"]["y"],
            ),
            destination=Location(
                id=message["destination"]["id"],
                x=message["destination"]["x"],
                y=message["destination"]["y"],
            ),
            neighbours=[
                Neighbour(
                    name=n["name"],
                    mac=n["mac"],
                    tq=n["tq"],
                    location=Location(
                        id=n["location"]["id"],
                        x=n["location"]["x"],
                        y=n["location"]["y"],
                    ),
                    last_seen=n["last_seen"]
                ) for n in message["neighbours"]
            ],
            transfered_files=message["transfered_files"]
        )
