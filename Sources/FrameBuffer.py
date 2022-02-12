from Buffer import Buffer
from Frame import Frame

class FrameBuffer(Buffer):
    def __init__(self):
        super().__init__()

    def add(self, data):
        assert isinstance(data, Frame), "[FrameBuffer::add]: invalid parameter type."
