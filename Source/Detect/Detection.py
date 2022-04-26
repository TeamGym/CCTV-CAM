from typing import List

from Core import Frame
from Detect import DetectionBox

class Detection:
    def __init__(self,
                 boxes : List[DetectionBox],
                 timestamp : int):
        self.__boxes = boxes
        self.__timestamp = timestamp

    def as_dict(self):
        return {
            'timestamp': self.timestamp,
            'boxes': [box.as_dict() for box in self.boxes]
        }

    @property
    def boxes(self):
        return self.__boxes

    @property
    def timestamp(self):
        return self.__timestamp
