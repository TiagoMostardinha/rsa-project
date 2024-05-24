import models.Location as Location
from dataclasses import dataclass
import json


@dataclass
class Neighbour():
    name: str
    tq: int
    location: Location

    def __json__(self):
        return {
            "name": self.name,
            "tq": self.tq,
            "location": self.location
        }
