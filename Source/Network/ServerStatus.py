from enum import Enum

class ServerStatusEnum(Enum):
    Unconnected = 1,
    TryingConnect = 2,
    Connected = 3

class ServerStatus:
    def __init__(self, value=ServerStatusEnum.Unconnected):
        self.__value = value

    def isUnconnected(self):
        return self.__value == ServerStatusEnum.Unconnected

    def isTryingConnect(self):
        return self.__value == ServerStatusEnum.TryingConnect

    def isConnected(self):
        return self.__value == ServerStatusEnum.Connected

    def setUnconnected(self):
        self.__value = ServerStatusEnum.Unconnected

    def setTryingConnect(self):
        self.__value = ServerStatusEnum.TryingConnect

    def setConnected(self):
        self.__value = ServerStatusEnum.Connected
