import time
import random

import cv2
import numpy as np

from Core.Frame import Frame
from Core.Buffer import Buffer

from Detect.DetectionBox import DetectionBox
from Detect.Detection import Detection

class ObjectDetector:
    def __init__(self, config, videoBuffer, outputBuffer, renderBuffer):
        self.__network = cv2.dnn.readNetFromDarknet(
            config.detector.object.config,
            config.detector.object.weights)
        self.__labels = open(config.detector.object.label).read().strip().split("\n")
        self.__confidenceThreshold = config.detector.object.threshold
        self.__layerNames = [self.__network.getLayerNames()[layer - 1]
                             for layer in self.__network.getUnconnectedOutLayers()]

        self.__colors = {}

        self.__videoBuffer = videoBuffer
        self.__outputBuffer = outputBuffer
        self.__renderBuffer = renderBuffer

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
        if self.__videoBuffer.size == 0:
            return

        startTime = time.time()

        frame = self.__videoBuffer.tail()
        self.__videoBuffer.clear()

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

        self.__outputBuffer.push(detection)
        self.__renderBuffer.push(resultFrame)
