from Core.FrameBuffer import FrameBuffer

class BufferMonitor:
    def __init__(self,
                 name: str,
                 buffer: FrameBuffer):
        self.__name = name
        self.__buffer = buffer

# ----------------------------------------------------------------------
# Property
# ----------------------------------------------------------------------

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        self.__name = value

    @property
    def buffer(self):
        return self.__buffer

    @buffer.setter
    def buffer(self, value):
        self.__buffer = value

    @property
    def width(self):
        return self.__buffer.width

    @property
    def height(self):
        return self.__buffer.height
