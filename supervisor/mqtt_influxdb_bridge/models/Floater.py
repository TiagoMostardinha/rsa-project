from models.Location import Location
import json

class Floater:
    id : str
    mac : str
    status : str
    location : Location
    files_to_tranfer : list[str]

    def __init__(self, id, mac, status, location, files_to_tranfer):
        self.id = id
        self.mac = mac
        self.status = status
        self.location = location
        self.files_to_tranfer = files_to_tranfer
    
    def toJSON(self):
        return {
            "id": self.id,
            "mac": self.mac,
            "status": self.status,
            "location": {
                "id": self.location.id,
                "x": self.location.x,
                "y": self.location.y
            },
            "files_to_tranfer": [
                f for f in self.files_to_tranfer
            ]
        }

    def fromJSON(data: dict):
        return Floater(
            id=data["id"],
            mac=data["mac"],
            status=data["status"],
            location=Location(
                id=data["location"]["id"],
                x=data["location"]["x"],
                y=data["location"]["y"]
            ),
            files_to_tranfer=data["files_to_tranfer"]
        )