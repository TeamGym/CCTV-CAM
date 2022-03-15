from Core.Buffer import Buffer

import cv2
import numpy as np
import pyglet
from pyglet.gl import *

import random
import ctypes

class Renderer(pyglet.window.Window):
    def __init__(self,
                 width : int,
                 height : int,
                 framerate : int,
                 frameBuffer : Buffer,
                 detectionBuffer : Buffer):
        super().__init__(width=width, height=height)

        pyglet.clock.schedule_interval(self.update, 1.0 / framerate)

        self.frameBuffer = frameBuffer
        self.detectionBuffer = detectionBuffer

        self.colors = {}

    def draw_box(self, image, box):
        x, y = box.x, box.y
        width, height = box.width, box.height
        left, right, top, bottom = x, x + width, y, y + height

        confidence = box.confidence
        classID = box.classID
        label = box.label

        if not label in self.colors:
            color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            self.colors[label] = color
        else:
            color = self.colors[label]

        text = "{}: {:.4f}".format(label, confidence)

        cv2.rectangle(image, (left, top), (right, bottom), color, 2)
        cv2.putText(image, text, (left, top - 5), cv2.FONT_HERSHEY_SIMPLEX,
                    0.5, color, 1)

    def update(self, deltaTime):
        pass

    def on_key_press(self, symbol, modifiers):
        symbol = chr(symbol)
        if symbol == 'q':
            self.close()

    def on_mouse_press(self, x, y, button, modifiers):
        pass

    def on_draw(self):
        pyglet.clock.tick()

        if self.frameBuffer.size == 0:
            return

        frame = self.frameBuffer.tail()
        image = frame.data
        image = image.copy()

        if self.detectionBuffer.size != 0:
            detection = self.detectionBuffer.tail()

            for box in detection.boxes:
                self.draw_box(image, box)

        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = np.flip(image, axis=0)

        glClearColor(0, 0, 0, 1)
        glClear(GL_COLOR_BUFFER_BIT)

        data = image.astype(np.uint8)
        dataPtr = data.ctypes.data_as(ctypes.POINTER(ctypes.c_ubyte))

        glDrawPixels(self.width, self.height, GL_RGB, GL_UNSIGNED_BYTE, dataPtr)
