from dataclasses import dataclass
import json

@dataclass
class Location():
    id: str
    x: int
    y: int

    def __json__(self):
        return {
            "id": self.id,
            "x": self.x,
            "y": self.y
        }