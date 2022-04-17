class BufferHolder:
    def __init__(self):
        self.__sockets = {}

    def socketExists(self, name):
        return name in self.__sockets

    def getSockets(self):
        return list(self.__sockets.keys())

    def getBuffer(self, name):
        if name in self.__sockets:
            return self.__sockets[name]

    def getBuffers(self):
        return list(self.__sockets.values())

    def connectBuffer(self, name, buffer):
        self.__sockets[name] = buffer

    def connectBuffers(self, sockets):
        assert(isinstance(sockets, dict))

        for name, buffer in sockets.items():
            self.connectBuffer(name, buffer)

    def removeBuffer(self, name):
        self.__sockets.pop(name)
