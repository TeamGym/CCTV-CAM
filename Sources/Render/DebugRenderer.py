from Core.Buffer import Buffer

import cv2
import matplotlib.pyplot as plt
import matplotlib.image as img

import random

class DebugRenderer:
    def __init__(self,
                 frameBuffer : Buffer,
                 detectionResultBuffer : Buffer):
        self.frameBuffer = frameBuffer
        self.detectionResultBuffer = detectionResultBuffer

        self.renderContext = None

        self.colors = {}
        
        self.__mode = "matplotlib"

    @property
    def mode(self):
        return self.__mode

    @mode.setter
    def mode(self, value):
        self.__mode = value

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
                
    def render(self):
        if self.frameBuffer.size == 0:
            return

        if self.mode == "opencv":
            self.render_opencv()
        elif self.mode == "matplotlib":
            self.render_matplotlib()

    def render_opencv(self):
        frame = self.frameBuffer.tail()
        image = frame.data

        image = image.copy()

        if self.detectionResultBuffer.size != 0:
            detectionResult = self.detectionResultBuffer.tail()

            for box in detectionResult.boxes:
                self.draw_box(image, box)

    def render_matplotlib(self):
        frame = self.frameBuffer.tail()
        timestamp = frame.timestamp
        
        image = frame.data
        image = image.copy()
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        if self.detectionResultBuffer.size != 0:
            detectionResult = self.detectionResultBuffer.tail()

            for box in detectionResult.boxes:
                self.draw_box(image, box)

        if self.renderContext == None:
            self.renderContext = plt.imshow(image)
            
        self.renderContext.set_array(image)
        plt.pause(0.0001)
