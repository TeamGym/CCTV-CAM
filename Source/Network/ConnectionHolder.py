from Network.ServerStatus import ServerStatus

class ConnectionHolder:
    def __init__(self):
        self.__connections = {}

    def connectionExists(self, name):
        assert isinstance(name, str)
        return name in self.__connections

    def getConnection(self, name):
        assert isinstance(name, str)

        if name in self.__connections:
            return self.__connections[name]

        return None

    def addConnection(self, name):
        assert isinstance(name, str)

        self.__connections[name] = ServerStatus()

    def addConnections(self, names):
        assert isinstance(names, list)

        for name in names:
            self.addConnection(name)

    def removeConnection(self, name):
        assert isinstance(name, str)

        self.__connections.pop(name)
