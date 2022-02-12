from Buffer import Buffer

from collections import deque

class CircularBuffer(Buffer):
    def __init__(self, maxlen):
        super().__init__()
        
        self.__maxlen = maxlen
        self.rawbuffer = deque(maxlen=maxlen)

    @property
    def size(self):
        return len(self.rawbuffer)

    @property
    def maxlen(self):
        return self.rawbuffer.maxlen
