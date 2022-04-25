import cv2
import time
import multiprocessing as mp

from Core.Frame import Frame
from Core.Buffer import Buffer

class VideoCapture:
    __startTime = time.time()

    def __init__(self, buffer=None):
        self.__cvCapture = None

        self.__width = 0
        self.__height = 0

        self.__frameRate = 0
        self.__frameDuration = 0
        self.__frameCount = 0

        if buffer is None:
            self.__buffer = Buffer(maxlen=1000)
        else:
            self.__buffer = buffer

        self.__isCapturing = False
        self.__isSimulatingFrameRate = True

# ----------------------------------------------------------------------
# Property
# ----------------------------------------------------------------------

    @property
    def width(self):
        return self.__width

    @property
    def height(self):
        return self.__height

    @property
    def frameCount(self):
        return self.__frameCount

    @property
    def frameRate(self):
        return self.__frameRate

    @frameRate.setter
    def frameRate(self, value):
        assert(isinstance(value, int))

        if not self.__isSimulatingFrameRate:
            return

        self.__frameRate = value
        self.__frameDuration = 1 / self.__frameRate

    @property
    def frameDuration(self):
        return self.__frameDuration

    @property
    def isCapturing(self):
        return self.__isCapturing

    @isCapturing.setter
    def isCapturing(self, value):
        assert(isinstance(value, bool))

        self.__isCapturing = value

    @property
    def isSimulatingFrameRate(self):
        return self.__isSimulatingFrameRate

    @isSimulatingFrameRate.setter
    def isSimulatingFrameRate(self, value):
        assert(isinstance(value, bool))

        self.__isSimulatingFrameRate = value

    @property
    def outputBuffer(self):
        return self.__buffer

    @outputBuffer.setter
    def outputBuffer(self, value):
        self.__buffer = value

    @property
    def timestamp(self):
        return time.time() - VideoCapture.__startTime

    @property
    def timestampMilliseconds(self):
        return int(self.timestamp * 1e3)

    @property
    def timestampMicroseconds(self):
        return int(self.timestamp * 1e6)

    @property
    def timestampNanoseconds(self):
        return int(self.timestamp * 1e9)

# ----------------------------------------------------------------------
# Private Member Method
# ----------------------------------------------------------------------

    def __waitUntilNextFrame(self, elapsedTime):

        if elapsedTime >= self.frameDuration:
            return

        time.sleep(self.frameDuration - elapsedTime)

# ----------------------------------------------------------------------
# Public Member Method
# ----------------------------------------------------------------------

    def openFile(self, fileName, width, height, frameRate):
        self.__width = width
        self.__height = height
        self.__frameRate = frameRate
        self.__frameDuration = 1 / self.__frameRate

        self.__cvCapture = cv2.VideoCapture(fileName)
        self.__cvCapture.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.__cvCapture.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
        self.__cvCapture.set(cv2.CAP_PROP_FPS, frameRate)

        self.__frameCount = 0

        self.isCapturing = True

    def openDevice(self, deviceName, width, height, frameRate):
        self.openFile(deviceName, width, height, frameRate)

    def openGstreamerPipeline(self, pipelineString, width, height, frameRate):
        self.__width = width
        self.__height = height
        self.__frameRate = frameRate
        self.__frameDuration = 1 / self.__frameRate

        self.__cvCapture = cv2.VideoCapture(pipelineString, cv2.CAP_GSTREAMER)

        self.__frameCount = 0

        self.isCapturing = True

    def close(self):
        self.__cvCapture.release()

    def read(self):
        startTime = time.time()

        if not self.isCapturing:
            self.__waitUntilNextFrame(0)

            return

        if not self.__cvCapture.isOpened():
            self.__waitUntilNextFrame(0)

            return

        ret, frame = self.__cvCapture.read()

        if not ret:
            self.__waitUntilNextFrame(0)

            return

        timestamp = self.timestamp

        frame = Frame(timestamp, frame)

        self.__buffer.push(frame)
        self.__frameCount += 1

        endTime = time.time()

        if self.__isSimulatingFrameRate:
            self.__waitUntilNextFrame(endTime - startTime)
