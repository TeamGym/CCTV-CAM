from Buffer import Buffer

import cv2
import matplotlib.pyplot as plt
import matplotlib.image as img

class DetectionRenderer:
    def __init__(self,
                 frameBuffer : Buffer,
                 detectionResultBuffer : Buffer):
        self.frameBuffer = frameBuffer
        self.detectionResultBuffer = detectionResultBuffer

        self.renderContext = None

    def render(self):
        if self.frameBuffer.size == 0:
            return
        
        frame = self.frameBuffer.tail()
        image = frame.data

        if self.detectionResultBuffer.size != 0:
            detectionResult = self.detectionResultBuffer.tail()

            for box in detectionResult.boxes:
                x, y = box.x, box.y
                width, height = box.width, box.height
                left, right, top, bottom = x, x + width, y, y + height

                confidence = box.confidence
                classID = box.classID
                label = box.label                

                color = 20

                text = "{}: {:.4f}".format(label, confidence)

                cv2.rectangle(image, (left, top), (right, bottom), color, 2)
                cv2.putText(image, text, (left, top - 5), cv2.FONT_HERSHEY_SIMPLEX,
                            0.5, color, 2)

        if self.renderContext == None:
            self.renderContext = plt.imshow(image)
            
        self.renderContext.set_array(image)
        plt.pause(0.0001)
