import cv2

class VideoWriter:
    def __init__(self):
        self.__cvWriter = None

        self.__width = 0
        self.__height = 0
        self.__fps = 0

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
    def fps(self):
        return self.__fps

# ----------------------------------------------------------------------
# Public Member Method
# ----------------------------------------------------------------------

    def openFile(self, fileName, fourcc, width, height, fps):
        self.__cvWriter = cv2.VideoWriter(
            fileName, cv2.VideoWriter_fourcc(*fourcc), fps, (width, height))

        self.__width = width
        self.__height = height
        self.__fps = fps

    def openDevice(self, deviceName, fourcc, width, height, fps):
        self.openFile(deviceName, fourcc, width, height, fps)

    def openGstreamerPipeline(self, pipelineString, fourcc, width, height, fps):
        self.__cvWriter = cv2.VideoWriter(
            pipelineString, cv2.VideoWriter_fourcc(*fourcc), fps, (width, height))

        self.__width = width
        self.__height = height
        self.__fps = fps

    def close(self):
        if self.__cvWriter is not None:
            self.__cvWriter.release()

    def write(self, image):
        self.__cvWriter.write(image)
