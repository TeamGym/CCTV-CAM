from typing import List

from DetectionBox import DetectionBox

class DetectionResult:
    def __init__(self,
                 timestamp : int,
                 boxes : List[DetectionBox]):
        self.timestamp = timestamp
        self.boxes = boxes

