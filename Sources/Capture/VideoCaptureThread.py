import sys

from threading import Thread

from Core.Buffer import Buffer
from Core.Frame import Frame

from Config.CameraConfig import CameraConfig

import cv2

import gi

gi.require_version('Gst', '1.0')
from gi.repository import Gst

class VideoCaptureThread(Thread):
    def __init__(self,
                 cameraConfig : CameraConfig,
                 frameBuffer : Buffer):
        super().__init__()

        self.device = cameraConfig.device
        self.width = cameraConfig.width
        self.height = cameraConfig.height
        self.fps = cameraConfig.fps
        self.format = cameraConfig.format

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

    def run(self):
        while True:
            if not self.capture.isOpened():
                continue

            ret, frame = self.capture.read()

            if not ret:
                continue

            timestamp = self.frameCount * self.duration
        
            frame = Frame(timestamp, frame)
            self.frameBuffer.add(frame)

            self.frameCount += 1
