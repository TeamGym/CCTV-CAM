from typing import List

import cv2
import numpy as np

import pyglet
from pyglet.gl import *
from pyglet.window import key as pyglet_key
import ctypes

from Render.RenderableMonitor import RenderableMonitor
from Render.BufferRenderer import BufferRenderer

class BufferViewer(BufferRenderer):
    def __init__(self,
                 fps: int,
                 monitors: List[RenderableMonitor]):
        super().__init__(fps, monitors)

        self.__bufferIndices = [0 for i in range(self.monitorCount)]
        self.__controllingMonitorIndex = 0
        self.__mode = "Renderer"

        self.addEventHandler("KeyDown", self.closeOnKey)
        self.addEventHandler("KeyDown", self.keyDownHandler)
        self.addEventHandler("KeyPress", self.keyPressHandler)
        self.addEventHandler("MouseDown", self.mouseDownHandler)
        self.addEventHandler("MouseDrag", self.mouseDragHandler)

# ----------------------------------------------------------------------
# Property
# ----------------------------------------------------------------------

    @property
    def mode(self):
        return self.__mode

    @mode.setter
    def mode(self, value):
        self.__mode = value

# ----------------------------------------------------------------------
# Event Handler
# ----------------------------------------------------------------------

    def closeOnKey(self, key):
        if key == pyglet_key.Q:
            self.close()

    def keyDownHandler(self, key):
        for i in range(10):
            if key == ord('1') + i:
                self.setControllingMonitorIndex(i)

    def keyPressHandler(self, key):
        if key == pyglet_key.LEFT:
            self.prevFrame()
        elif key == pyglet_key.RIGHT:
              self.nextFrame()

    def mouseDownHandler(self, x, y, button):
        y = self.height - y

        if button == 1:
            for i in range(self.monitorCount):
                monitor = self.monitors[i]

                left = monitor.left
                top = monitor.top
                right = left + monitor.width
                bottom = top + monitor.height

                if x >= left and x <= right and y >= top and y <= bottom:
                    self.setControllingMonitorIndex(i)

    def mouseDragHandler(self, x, y, dx, dy, button):
        if button == 1:
            for i in range(0, dx):
                self.nextFrame()

            for i in range(0, -dx):
                self.prevFrame()

# ----------------------------------------------------------------------
# Monitor Control
# ----------------------------------------------------------------------

    def setControllingMonitorIndex(self, index):
        if index < 0 or index >= self.monitorCount:
            return

        self.__controllingMonitorIndex = index

    def prevFrame(self):
        monitorIndex = self.__controllingMonitorIndex
        if monitorIndex >= self.monitorCount:
            return

        monitor = self.monitors[monitorIndex]

        buffer = monitor.buffer
        bufferIndex = self.__bufferIndices[monitorIndex]
        if bufferIndex >= buffer.size:
            return

        self.__bufferIndices[monitorIndex] = max(0, bufferIndex - 1)

    def nextFrame(self):
        monitorIndex = self.__controllingMonitorIndex
        if monitorIndex >= self.monitorCount:
            return

        monitor = self.monitors[monitorIndex]

        buffer = monitor.buffer
        bufferIndex = self.__bufferIndices[monitorIndex]
        if bufferIndex >= buffer.size:
            return

        self.__bufferIndices[monitorIndex] = min(buffer.size - 1, bufferIndex + 1)

# ----------------------------------------------------------------------
# Render Method
# ----------------------------------------------------------------------

    def drawName(self, image, name):
        text = "monitor: {}".format(name)

        cv2.putText(image, text, (0, 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (50, 200, 50), 1)

    def drawTimestamp(self, image, timestamp):
        text = "timestamp: {:.2f}s".format(timestamp)

        cv2.putText(image, text, (0, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (50, 200, 50), 1)

    def getMonitorFrames(self):
        if self.mode == "Renderer":
            return self.getFramesRenderer()
        elif self.mode == "Viewer":
            return self.getFramesViewer()
        else:
            return []

    def getFramesViewer(self):
        frames = []

        monitorIndex = 0
        for monitor in self.monitors:
            buffer = monitor.buffer

            bufferIndex = self.__bufferIndices[monitorIndex]

            if monitor.buffer.size <= bufferIndex:
                continue

            frame = buffer.get(bufferIndex)
            image = frame.data
            image = image.copy()

            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

            (height, width, _) = image.shape

            self.drawName(image, monitor.name)
            self.drawTimestamp(image, frame.timestamp)

            if monitorIndex == self.__controllingMonitorIndex:
                cv2.rectangle(
                    image, (0, 0), (width - 2, height - 2), (255, 0, 255), 2)

            image = np.flip(image, axis=0)
            image = cv2.resize(image,
                               dsize=(monitor.width,
                                      monitor.height),
                               interpolation=cv2.INTER_LINEAR)

            frames.append(image)

            monitorIndex += 1

        return frames

    def getFramesRenderer(self):
        frames = []

        for monitor in self.monitors:
            if monitor.buffer.size == 0:
                continue

            frame = monitor.buffer.tail()
            image = frame.data
            image = image.copy()

            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

            self.drawName(image, monitor.name)
            self.drawTimestamp(image, frame.timestamp)

            image = np.flip(image, axis=0)
            image = cv2.resize(image,
                               dsize=(monitor.width,
                                      monitor.height),
                               interpolation=cv2.INTER_LINEAR)

            frames.append(image)

        return frames
