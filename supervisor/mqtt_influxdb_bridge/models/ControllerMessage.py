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
    inRange: list       # List of inRange Neighbors
    stopFlag: bool

    def __json__(self):
        return {
            "typeOfMessage": self.typeOfMessage,
            "startFlag": self.startFlag,
            "startLocation": self.startLocation.__json__() if self.startLocation else None,
            "destLocation": self.destLocation.__json__() if self.destLocation else None,
            "inRange": self.inRange,
            "stopFlag": self.stopFlag
        }
