from Core.Buffer import Buffer

import cv2
import numpy as np
import pyglet
from pyglet.gl import *

import random
import ctypes

class Renderer(pyglet.window.Window):
    def __init__(self, context):
        super().__init__(width=context.width, height=context.height)

        pyglet.clock.schedule_interval(self.update, 1.0 / context.fps)

        self.__frameBuffer = context.frameBuffer
        self.__detectionBuffer = context.detectionBuffer

        self.__colors = {}

    def draw_box(self, image, box):
        x, y = box.x, box.y
        width, height = box.width, box.height
        left, right, top, bottom = x, x + width, y, y + height

        confidence = box.confidence
        classID = box.classID
        label = box.label

        if not label in self.__colors:
            color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            self.__colors[label] = color
        else:
            color = self.__colors[label]

        text = "{}: {:.4f}".format(label, confidence)

        cv2.rectangle(image, (left, top), (right, bottom), color, 2)
        cv2.putText(image, text, (left, top - 5), cv2.FONT_HERSHEY_SIMPLEX,
                    0.5, color, 1)

    def draw_timestamp(self, image, timestamp):
        text = "timestamp: {:.2f}ms".format(timestamp / 1e6)

        cv2.putText(image, text, (0, 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

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

        if self.__frameBuffer.size == 0:
            return

        frame = self.__frameBuffer.tail()
        image = frame.data
        image = image.copy()

        if self.__detectionBuffer.size != 0:
            detection = self.__detectionBuffer.tail()

            for box in detection.boxes:
                self.draw_box(image, box)

        self.draw_timestamp(image, frame.timestamp)

        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = np.flip(image, axis=0)

        glClearColor(0, 0, 0, 1)
        glClear(GL_COLOR_BUFFER_BIT)

        data = image.astype(np.uint8)
        dataPtr = data.ctypes.data_as(ctypes.POINTER(ctypes.c_ubyte))

        glDrawPixels(self.width, self.height, GL_RGB, GL_UNSIGNED_BYTE, dataPtr)
