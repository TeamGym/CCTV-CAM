from Core.CircularBuffer import CircularBuffer
from Core.Frame import Frame

class FrameBuffer(CircularBuffer):
    def __init__(self, width, height, maxlen):
        super().__init__(maxlen)

        self.__width = width
        self.__height = height

    @property
    def width(self):
        return self.__width

    @property
    def height(self):
        return self.__height

    def push(self, frame):
        assert isinstance(frame, Frame)
        assert frame.data.shape[:2] == (self.height, self.width)

        self.rawbuffer.append(frame)
