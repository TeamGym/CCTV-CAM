import cv2
import numpy as np

from threading import Thread

from Core.Buffer import Buffer
from Core.Frame import Frame

from Detect.DetectionBox import DetectionBox
from Detect.Detection import Detection

class Detector(Thread):
    def __init__(self,
                 labelFileName : str,
                 configFileName : str,
                 weightsFileName : str,
                 confidenceThreshold : int,
                 frameBuffer : Buffer,
                 detectionBuffer : Buffer):
        super().__init__()

        self.network = cv2.dnn.readNetFromDarknet(configFileName, weightsFileName)
        self.labels = open(labelFileName).read().strip().split("\n")        
        self.confidenceThreshold = confidenceThreshold
        self.layerNames = [self.network.getLayerNames()[layer - 1] for layer in self.network.getUnconnectedOutLayers()]

        self.frameBuffer = frameBuffer
        self.detectionBuffer = detectionBuffer

    def detect(self):
        if self.frameBuffer.size == 0:
            return

        frame = self.frameBuffer.tail()

        timestamp = frame.timestamp
        image = frame.data

        (H, W) = image.shape[:2]

        blob = cv2.dnn.blobFromImage(image, 1 / 255.0, (416, 416), swapRB=True, crop=False)
        self.network.setInput(blob)

        layerOutputs = self.network.forward(self.layerNames)

        boxes = []
        classIDs = []
        confidences = []

        for output in layerOutputs:
            for detection in output:
                scores = detection[5:]
                classID = np.argmax(scores)
                confidence = scores[classID]

                if confidence > self.confidenceThreshold:
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
                                self.confidenceThreshold,
                                self.confidenceThreshold)

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
                    self.labels[classID])
                detectionBoxes.append(detectionBox)

        detection = Detection(detectionBoxes, timestamp)
        self.detectionBuffer.add(detection)

        #print("[DetectionThread]: Object detection completed.(timestamp: {}, boxes: {})".format(timestamp, len(detectionBoxes)))
