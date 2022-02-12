import cv2
import numpy as np

from threading import Thread

from Frame import Frame
from FrameBuffer import FrameBuffer

from DetectionBox import DetectionBox
from DetectionResult import DetectionResult
from DetectionResultBuffer import DetectionResultBuffer

class DetectionThread(Thread):
    def __init__(self,
                 labelFileName : str,
                 configFileName : str,
                 weightsFileName : str,
                 confidenceThreshold : int,
                 frameBuffer : FrameBuffer,
                 detectionResultBuffer : DetectionResultBuffer):
        super().__init__()

        self.network = cv2.dnn.readNetFromDarknet(configFileName, weightsFileName)
        self.labels = open(labelFileName).read().strip().split("\n")        
        self.confidenceThreshold = confidenceThreshold
        self.layerNames = [self.network.getLayerNames()[layer - 1] for layer in self.network.getUnconnectedOutLayers()]

        self.frameBuffer = frameBuffer
        self.detectionResultBuffer = detectionResultBuffer

    def run(self):
        while True:
            if frameBuffer.size() == 0:
                continue

            frame = frameBuffer.pop(0)

            timestamp = frame.timestamp
            data = frame.data

            (H, W) = data.shape[:2]

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
                        
            idxs = cv2.dnn.NMSBoxes(boxes,
                                    confidences,
                                    self.confidenceThreshold,
                                    self.confidenceThreshold)

            detectionBoxes = []
            for i in idxs.flatten():
                box = boxes[i]
                (x, y, w, h) = (box[0], box[1], box[2], box[3])

                confidence = confidences[i]
                classID = classIDs[i]

                detectionBox = DetectionBox(
                    x, y, w, h,
                    confidence,
                    classID)
                detectionBoxes.append(detectionBox)

            detectionResult = DetectionResult(detectionBoxes, frame)
            self.detectionResultBuffer.add(detectionResult)
