import cv2

class VideoWriter:
    def __init__(self):
        self.__cvWriter = None

        self.__width = 0
        self.__height = 0
        self.__frameRate = 0

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
    def frameRate(self):
        return self.__frameRate

# ----------------------------------------------------------------------
# Public Member Method
# ----------------------------------------------------------------------

    def openFile(self, fileName, fourccString, width, height, frameRate):
        self.__cvWriter = cv2.VideoWriter(
            fileName, cv2.VideoWriter_fourcc(*fourccString), frameRate, (width, height))

        self.__width = width
        self.__height = height
        self.__frameRate = frameRate

    def openDevice(self, deviceName, fourccString, width, height, frameRate):
        self.openFile(deviceName, fourccString, width, height, frameRate)

    def openGstreamerPipeline(self, pipelineString, fourccString, width, height, frameRate):
        self.__cvWriter = cv2.VideoWriter(
            pipelineString, cv2.VideoWriter_fourcc(*fourccString), frameRate, (width, height))

        self.__width = width
        self.__height = height
        self.__frameRate = frameRate

    def close(self):
        self.__cvWriter.release()

    def write(self, image):
        self.__cvWriter.write(image)
