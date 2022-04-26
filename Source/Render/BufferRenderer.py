from typing import List
import cv2
import numpy as np

import pyglet
from pyglet.gl import *
from pyglet.window import key as pyglet_key
import ctypes

from . import Window, RenderableMonitor

class BufferRenderer(Window):
    def __init__(self,
                 fps: int,
                 monitors: List[RenderableMonitor]) -> None:
        windowWidth = 0
        windowHeight = 0

        self.__monitors = monitors

        for monitor in self.__monitors:
            monitorLeft = monitor.left
            monitorTop = monitor.top
            monitorWidth = monitor.width
            monitorHeight = monitor.height

            monitorRight = monitorLeft + monitorWidth
            monitorBottom = monitorTop + monitorHeight

            windowWidth = max(windowWidth, monitorRight)
            windowHeight = max(windowHeight, monitorBottom)

        super().__init__(windowWidth, windowHeight, fps)

        self.addEventHandler("KeyDown", self.closeOnKey)

# ----------------------------------------------------------------------
# Property
# ----------------------------------------------------------------------

    @property
    def monitors(self):
        return self.__monitors

    @property
    def monitorCount(self):
        return len(self.__monitors)

# ----------------------------------------------------------------------
# Public Member Method
# ----------------------------------------------------------------------

    def closeOnKey(self, key) -> None:
        if key == pyglet_key.Q:
            self.close()

    def getMonitorFrames(self):
        return []

    def on_draw(self) -> None:
        pyglet.clock.tick()

        glClearColor(0, 0, 0, 1)
        glClear(GL_COLOR_BUFFER_BIT)

        monitorFrames = self.getMonitorFrames()

        if len(monitorFrames) != self.monitorCount:
            return

        renderResult = np.zeros((self.height, self.width, 3), np.uint8)
        for i in range(self.monitorCount):
            monitor = self.monitors[i]
            frame = monitorFrames[i]

            left = monitor.left
            right = monitor.right
            top = monitor.top
            bottom = monitor.bottom

            width = monitor.width
            height = monitor.height

            renderResult[top:bottom, left:right] = frame

        data = renderResult.astype(np.uint8)
        dataPtr = data.ctypes.data_as(ctypes.POINTER(ctypes.c_ubyte))

        glPixelStorei(GL_UNPACK_ALIGNMENT, 1)

        glDrawPixels(self.width,
                     self.height,
                     GL_RGB,
                     GL_UNSIGNED_BYTE,
                     dataPtr)
