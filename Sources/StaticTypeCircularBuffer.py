from Buffer import Buffer
from CircularBuffer import CircularBuffer

from collections import deque

class StaticTypeCircularBuffer(CircularBuffer):
    def __init__(self, elementType, maxlen):
        super().__init__(maxlen)

        self.__elementType = elementType

    @property
    def elementType(self):
        return self.__elementType

    def add(self, data):
        assert isinstance(data, self.__elementType), "[StaticTypeCircularBuffer::add] Invalid type."
        
        self.rawbuffer.append(data)
