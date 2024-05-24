from models.Location import Location
from models.Neighbour import Neighbour
from dataclasses import dataclass
import json


@dataclass
class ControllerMessage():
    typeOfMessage: str
    startFlag: bool
    startLocation: Location
    destLocation: Location
    map: list
    inRange: list       # List of inRange Neighbors
    stopFlag: bool

    def __json__(self):
        return {
            "typeOfMessage": self.typeOfMessage,
            "startFlag": self.startFlag,
            "startLocation": self.startLocation.__json__(),
            "destLocation": self.destLocation.__json__(),
            "map": self.map,
            "inRange": [d for d in self.inRange],
            "stopFlag": self.stopFlag
        }

