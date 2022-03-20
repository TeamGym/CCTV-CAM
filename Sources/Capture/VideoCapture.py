import sys

from threading import Thread

from Core.Buffer import Buffer
from Core.Frame import Frame

import cv2

import gi

gi.require_version('Gst', '1.0')
from gi.repository import Gst

class VideoCapture(object):
    def __init__(self, context):
        super().__init__()

        self.__device = context.device
        self.__width = context.width
        self.__height = context.height
        self.__fps = context.fps
        self.__format = context.colorFormat

        self.__duration = 1 / self.__fps * Gst.SECOND
        self.__frameCount = 0

        self.ready()

        self.__frameBuffer = context.frameBuffer

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
    def format(self):
        return self.__format

    def ready(self):
        self.__cvCapture = cv2.VideoCapture(self.__device)
        self.__cvCapture.set(cv2.CAP_PROP_FRAME_WIDTH, self.__width)
        self.__cvCapture.set(cv2.CAP_PROP_FRAME_HEIGHT, self.__height)
        self.__cvCapture.set(cv2.CAP_PROP_FPS, self.__fps)

        if not self.__cvCapture.isOpened():
            print("[cv2.VideoCvCapture]: can't open")
            sys.exit()

    def read(self):
        if not self.__cvCapture.isOpened():
            return

        ret, frame = self.__cvCapture.read()

        if not ret:
            return

        timestamp = self.__frameCount * self.__duration

        frame = Frame(timestamp, frame)
        self.__frameBuffer.add(frame)

        self.__frameCount += 1
