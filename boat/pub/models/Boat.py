from models.Location import Location
from models.Neighbour import Neighbour


class Boat:
    id: str
    status: str
    speed: int
    direction: int
    location: Location
    destination: Location
    neighbours: list
    transfered_files: list[str]

    def __init__(self, id, status, speed, direction, location, neighbours, destination, transfered_files):
        self.id = id
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
            "status": self.status,
            "speed": self.speed,
            "direction": self.direction,
            "location": {
                "id": self.location.id,
                "x": self.location.x,
                "y": self.location.y
            },
            "destination": {
                "id": self.destination.id,
                "x": self.destination.x,
                "y": self.destination.y
            },
            "neighbours": [
                {
                    "name": n.name,
                    "tq": n.tq,
                    "location": {
                        "id": n.location.id,
                        "x": n.location.x,
                        "y": n.location.y
                    }
                } for n in self.neighbours
            ],
            "transfered_files": [
                f for f in self.transfered_files
            ] 
        }

    def fromJSON(message):
        return Boat(
            id=message["id"],
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
                    tq=n["tq"],
                    location=Location(
                        id=n["location"]["id"],
                        x=n["location"]["x"],
                        y=n["location"]["y"],
                    )
                ) for n in message["neighbours"]
            ],
            transfered_files=message["transfered_files"]
        )