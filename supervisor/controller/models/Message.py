from dataclasses import dataclass
import json


@dataclass
class Message:
    content: str
    source: str

    def __str__(self):
        return f'{self.source} {self.content}'


@dataclass
class ErrorMessage(Message):
    errorVar: str
    errorCode: int

    def __str__(self):
        return f'({self.errorVar} {self.errorCode}) {self.source} {self.content}'


@dataclass
class View():
    x: int
    y: int


@dataclass
class Neighbour():
    name: str
    distance: int


@dataclass
class BoatContent():
    speed: int
    direction: int
    location: View
    neighbours: list[Neighbour]
    transfered_files: int


@dataclass
class BoatMessage(Message):
    destination: View
    status: str
    content: BoatContent


@dataclass
class FloaterMessage(Message):
    pass


def toJSON(boat) -> dict:
    neighbours = []
    for n in boat.content.neighbours:
        neighbours.append(
            {
                "name": n.name,
                "distance": n.distance
            }
        )

    msg = {
        "source": boat.source,
        "destination": {
            "x": boat.destination.x,
            "y": boat.destination.y
        },
        "status": boat.status,
        "content": {
            "speed": boat.content.speed,
            "direction": boat.content.direction,
            "location": {
                "x": boat.content.location.x,
                "y": boat.content.location.y
            },
            "neighbours": neighbours,
            "transfered_files": boat.content.transfered_files
        }
    }
    return msg


def fromJSON(message) -> BoatMessage:

    neighbours = []
    for n in message["content"]["neighbours"]:
        neighbours.append(
            Neighbour(
                name=n["name"],
                distance=n["distance"]
            )
        )

    return BoatMessage(
        source=message["source"],
        destination=View(x=message["destination"]
                         ["x"], y=message["destination"]["y"]),
        status=message["status"],
        content=BoatContent(
            speed=message["content"]["speed"],
            direction=message["content"]["direction"],
            location=View(x=message["content"]["location"]
                          ["x"], y=message["content"]["location"]["y"]),
            neighbours=neighbours,
            transfered_files=message["content"]["transfered_files"]
        )
    )


@dataclass
class ControllerMessage(Message):
    inRange :bool