from enum import Enum

from .Rsp import Rsp

class Request:
    def __init__(self, method, onResponseCallback=None, properties={}):
        self.__method = method
        self.__delivered = False
        self.__onResponseCallback = onResponseCallback
        self.__properties = properties
        self.__sequence = 0
        self.__remoteAddress = None

    @property
    def delivered(self):
        return self.__delivered

    @delivered.setter
    def delivered(self, value):
        self.__delivered = value

    @property
    def onResponseCallback(self):
        return self.__onResponseCallback

    @onResponseCallback.setter
    def onResponseCallback(self, value):
        self.__onResponseCallback = value

    @property
    def method(self):
        return self.__method

    @method.setter
    def method(self, value):
        self.__method = value

    @property
    def sequence(self):
        return self.__sequence

    @sequence.setter
    def sequence(self, value):
        self.__sequence = value

    @property
    def remoteAddress(self):
        return self.__remoteAddress

    @remoteAddress.setter
    def remoteAddress(self, value):
        self.__remoteAddress = value

    def getProperties(self):
        return self.__properties.keys()

    def getProperty(self, key):
        return self.__properties.get(key)

    def addProperty(self, key, value):
        self.__properties[key] = value

    def getMessageString(self):
        requestLine = self.__method.name + ' RSP/' + Rsp.VERSION + '\n'
        sequenceLine = 'Seq=' + str(self.__sequence) + '\n'
        propertyLines = []

        for name, value in self.__properties.items():
            propertyLines.append(name + '=' + value + '\n')

        return requestLine \
                + sequenceLine \
                + ''.join(propertyLines) \
                + '\n'

    class Method(Enum):
        GET_INFO = 1
        JOIN = 2
        CONTROL_AUDIO = 3
