from Frame import Frame
from DetectionBox import DetectionBox

class DetectionResult:
    def __init__(self,
                 boxes : list[DetectionBox],
                 frame : Frame):
        self.boxes = boxes

        self.frame = frame
        self.timestamp = frame.timestamp
        self.data = frame.data
