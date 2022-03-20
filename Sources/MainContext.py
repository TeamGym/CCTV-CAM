from Core.StaticTypeCircularBuffer import StaticTypeCircularBuffer
from Core.Frame import Frame
from Detect.Detection import Detection
from queue import Queue

class MainContext:
    def __init__(self,
                 device : str,
                 width : int,
                 height : int,
                 fps : int,
                 colorFormat : str,
                 rtspLocation : str,
                 tcpHost : str,
                 tcpPort : int):
        self.__device = device
        self.__width = width
        self.__height = height
        self.__fps = fps
        self.__colorFormat = colorFormat
        self.__rtspLocation = rtspLocation
        self.__tcpHost = tcpHost
        self.__tcpPort = tcpPort

        self.__frameBuffer = StaticTypeCircularBuffer(Frame, 64)
        self.__differenceBuffer = StaticTypeCircularBuffer(Frame, 64)
        self.__detectionBuffer = StaticTypeCircularBuffer(Detection, 64)
        self.__commandQueue = Queue()

        self.__rtspStatus = "Unconnected"
        self.__tcpStatus = "Unconnected"

    @property
    def device(self):
        return self.__device

    @property
    def width(self):
        return self.__width

    @property
    def height(self):
        return self.__height

    @property
    def fps(self):
        return self.__fps

    @property
    def colorFormat(self):
        return self.__colorFormat

    @property
    def rtspLocation(self):
        return self.__rtspLocation

    @property
    def tcpHost(self):
        return self.__tcpHost

    @property
    def tcpPort(self):
        return self.__tcpPort

    @property
    def frameBuffer(self):
        return self.__frameBuffer

    @property
    def differenceBuffer(self):
        return self.__differenceBuffer

    @property
    def detectionBuffer(self):
        return self.__detectionBuffer

    @property
    def commandQueue(self):
        return self.__commandQueue

    @property
    def rtspStatus(self):
        return self.__rtspStatus

    @property
    def tcpStatus(self):
        return self.__tcpStatus

    @rtspStatus.setter
    def rtspStatus(self, value):
        self.__rtspStatus = value

    @tcpStatus.setter
    def tcpStatus(self, value):
        self.__tcpStatus = value
