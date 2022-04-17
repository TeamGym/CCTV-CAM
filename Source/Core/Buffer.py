from collections import deque

class Buffer:
    def __init__(self, maxlen=-1):
        assert maxlen >= -1

        if maxlen < 0:
            self.__buffer = deque()
        else:
            self.__buffer = deque(maxlen=maxlen)

    @property
    def size(self):
        return len(self.__buffer)

    @property
    def maxlen(self):
        return self.__buffer.maxlen

    @property
    def rawbuffer(self):
        return self.__buffer

    @rawbuffer.setter
    def rawbuffer(self, value):
        self.__buffer = value

    def clear(self):
        self.__buffer.clear()

    def get(self, index):
        return self.__buffer[index]

    def push(self, data):
        self.__buffer.append(data)

    def pop(self, index=-1):
        return self.__buffer.pop(index)

    def insert(self, index, data):
        self.__buffer.insert(index, data)

    def first(self):
        return self.__buffer[0]

    def last(self):
        return self.__buffer[self.size - 1]

    def head(self):
        return self.first()

    def tail(self):
        return self.last()
