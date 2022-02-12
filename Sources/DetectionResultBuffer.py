from Buffer import Buffer
from DetectionResult import DetectionResult

class DetectionResultBuffer(Buffer):
    def __init__(self):
        super().__init__()

    def add(self, data):
        assert isinstance(data, DetectionResultBuffer), "[DetectionResultBuffer::add]: invalid parameter type."

