import cv2

class Frame:
    def __init__(self, timestamp, data):
        self.__timestamp = timestamp
        self.__data = data

    @property
    def timestamp(self):
        return self.__timestamp

    @timestamp.setter
    def timestamp(self, value):
        self.__timestamp = value

    @property
    def data(self):
        return self.__data

    @data.setter
    def data(self, value):
        self.__data = value
