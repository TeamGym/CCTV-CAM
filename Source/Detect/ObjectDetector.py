import cv2
import numpy as np
import random

from Core.Frame import Frame
from Core.FrameBuffer import FrameBuffer

from Detect.DetectionBox import DetectionBox
from Detect.Detection import Detection

class ObjectDetector:
    def __init__(self,
                 labelFileName : str,
                 configFileName : str,
                 weightsFileName : str,
                 confidenceThreshold : int,
                 context):
        self.__network = cv2.dnn.readNetFromDarknet(configFileName, weightsFileName)
        self.__labels = open(labelFileName).read().strip().split("\n")
        self.__confidenceThreshold = confidenceThreshold
        self.__layerNames = [self.__network.getLayerNames()[layer - 1] for layer in self.__network.getUnconnectedOutLayers()]
        self.__colors = {}

        self.__readBuffer = context.frameBuffer
        self.__writeBuffer = context.detectionBuffer
        self.__monitorBuffer = FrameBuffer(width=context.width,
                                           height=context.height,
                                           maxlen=500)



    @property
    def network(self):
        return self.__network

    @property
    def labels(self):
        return self.__labels

    @property
    def confidenceThreshold(self):
        return self.__confidenceThreshold

    @confidenceThreshold.setter
    def confidenceThreshold(self, value):
        self.__confidenceThreshold = value

    @property
    def readBuffer(self):
        return self.__readBuffer

    @property
    def writeBuffer(self):
        return self.__writeBuffer

    @property
    def monitorBuffer(self):
        return self.__monitorBuffer

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


    def detect(self):
        if self.__readBuffer.size == 0:
            return

        frame = self.__readBuffer.tail()

        timestamp = frame.timestamp
        image = frame.data

        (H, W) = image.shape[:2]

        blob = cv2.dnn.blobFromImage(image, 1 / 255.0, (416, 416), swapRB=True, crop=False)
        self.__network.setInput(blob)

        layerOutputs = self.__network.forward(self.__layerNames)

        boxes = []
        classIDs = []
        confidences = []

        for output in layerOutputs:
            for detection in output:
                scores = detection[5:]
                classID = np.argmax(scores)
                confidence = scores[classID]

                if confidence > self.__confidenceThreshold:
                    box = detection[:4] * np.array([W, H, W, H])
                    (centerX, centerY, width, height) = box.astype('int')

                    x = int(centerX - width / 2)
                    y = int(centerY - height / 2)

                    width = int(width)
                    height = int(height)

                    boxes.append([x, y, width, height])
                    confidences.append(float(confidence))
                    classIDs.append(classID)

        idxs = cv2.dnn.NMSBoxes(boxes,
                                confidences,
                                self.__confidenceThreshold,
                                self.__confidenceThreshold)

        detectionBoxes = []

        if len(idxs) > 0:
            for i in idxs.flatten():
                box = boxes[i]
                (x, y, w, h) = (box[0], box[1], box[2], box[3])

                confidence = confidences[i]
                classID = classIDs[i]

                detectionBox = DetectionBox(
                    x, y, w, h,
                    confidence,
                    classID,
                    self.__labels[classID])
                detectionBoxes.append(detectionBox)

        detection = Detection(detectionBoxes, timestamp)

        resultImage = image.copy()
        resultFrame = Frame(frame.timestamp, resultImage)

        for box in detectionBoxes:
            self.draw_box(resultImage, box)

        self.__writeBuffer.push(detection)
        self.__monitorBuffer.push(resultFrame)

        #print("[DetectionThread]: Object detection completed.(timestamp: {}, boxes: {})".format(timestamp, len(detectionBoxes)))
