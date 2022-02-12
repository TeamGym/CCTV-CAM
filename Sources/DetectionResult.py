from typing import List

from Frame import Frame
from DetectionBox import DetectionBox

class DetectionResult:
    def __init__(self,
                 boxes : List[DetectionBox],
                 timestamp : int):
        self.__boxes = boxes
        self.__timestamp = timestamp

    @property
    def boxes(self):
        return self.__boxes

    @property
    def timestamp(self):
        return self.__timestamp
