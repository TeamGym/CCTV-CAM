import sys

from threading import Thread

from Core.Buffer import Buffer
from Core.Frame import Frame

import cv2

import gi

gi.require_version('Gst', '1.0')
from gi.repository import Gst

class VideoCapture(object):
    def __init__(self,
                 device : str = "/dev/video0",
                 width : int = 640,
                 height : int = 480,
                 fps : int = 30,
                 format : str = "YUY2",
                 frameBuffer : Buffer = None):
        super().__init__()

        self.device = device
        self.width = width
        self.height = height
        self.fps = fps
        self.format = format
        self.capture = cv2.VideoCapture(self.device)
        self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
        self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)
        self.capture.set(cv2.CAP_PROP_FPS, self.fps)

        self.duration = 1 / self.fps * Gst.SECOND
        self.frameCount = 0

        if not self.capture.isOpened():
            print("[cv2.VideoCapture]: can't open")
            sys.exit()

        self.frameBuffer = frameBuffer

    def read(self):
        if not self.capture.isOpened():
            return

        ret, frame = self.capture.read()

        if not ret:
            return

        timestamp = self.frameCount * self.duration

        frame = Frame(timestamp, frame)
        self.frameBuffer.add(frame)

        self.frameCount += 1
