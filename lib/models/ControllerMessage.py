from dataclasses import dataclass
import json


@dataclass
class ControllerMessage():
    typeOfMessage: str
    inRange: list       # List of inRange Neighbors

    def __json__(self):
        return {
            "typeOfMessage": self.typeOfMessage,
            "inRange": self.inRange,
        }
