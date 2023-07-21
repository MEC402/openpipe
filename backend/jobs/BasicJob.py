from abc import ABC
from datetime import datetime, timezone


class BasicJob(ABC):

    def __init__(self):
        self.status = "Initiated"
        self.launchTime = None
        self.endTime = None
        self.description = ""

    def runJob(self):
        pass

    def getJobDetails(self):
        return {"status": self.status,
                "launchTime": self.launchTime,
                "endTime": self.endTime,
                "description": self.description}
