import time

import cv2
import numpy as np

from Core.Buffer import Buffer
from Core.Frame import Frame

class MotionDetector:
    def __init__(self,
                 readBuffer: Buffer,
                 writeBuffer: Buffer):
        self.__readBuffer = readBuffer
        self.__writeBuffer = writeBuffer

        self.__referenceFrame = None

        self.__latestFrame = None
        self.__latestFrameCount = 0
        self.__latestFrameRMSSum = 0

        self.__frameCount = 0

        self.__fps = 30
        self.__duration = 1 / 30

    @property
    def readBuffer(self):
        return self.__readBuffer

    @readBuffer.setter
    def readBuffer(self, value):
        self.__readBuffer = value

    @property
    def writeBuffer(self):
        return self.__writeBuffer

    @writeBuffer.setter
    def writeBuffer(self, value):
        self.__writeBuffer = value

    def detect(self):
        if self.__readBuffer.size == 0:
            return

        startTime = time.time()

        frame = self.__readBuffer.tail()
        timestamp = frame.timestamp
        image = frame.data

        blurredImage = cv2.GaussianBlur(image, (5, 5), 0)

        grayImage = cv2.cvtColor(blurredImage, cv2.COLOR_BGR2GRAY)
        grayFrame = Frame(timestamp, grayImage)

        if self.__referenceFrame is None:
            self.__referenceFrame = grayFrame

        if self.__latestFrame is None:
            self.__latestFrame = grayFrame

        referenceDiff = cv2.absdiff(grayImage, self.__referenceFrame.data)
        referenceRMS = np.sqrt(cv2.mean(cv2.pow(referenceDiff, power=2))[0])

        latestDiff = cv2.absdiff(grayImage, self.__latestFrame.data)
        latestRMS = np.sqrt(cv2.mean(cv2.pow(latestDiff, power=2))[0])

        self.__latestFrameRMSSum += latestRMS

        if self.__latestFrameCount % 60 == 0:

            if self.__latestFrameRMSSum <= 60 * 4.0:
                self.__referenceFrame = grayFrame

            """
            print("referenceRMS: {}\n"
                  "latestRMS: {}\n"
                  "letestFrameRMSSum: {}\n"
                  "latestFrameCount: {}\n"
                  .format(referenceRMS,
                          latestRMS,
                          self.__latestFrameRMSSum,
                          self.__latestFrameCount))
            """

            self.__latestFrameCount = 0
            self.__latestFrameRMSSum = 0

            self.__latestFrame = grayFrame

        _, diffThreshold = cv2.threshold(referenceDiff, 10, 255, cv2.THRESH_BINARY)

        mask = cv2.dilate(diffThreshold, (5, 5), iterations=2)
        mask = cv2.cvtColor(diffThreshold, cv2.COLOR_GRAY2RGB)

        maskedImage = cv2.bitwise_and(image, mask)
        maskedFrame = Frame(timestamp, maskedImage)

        self.__writeBuffer.add(maskedFrame)

        self.__latestFrameCount += 1
        self.__frameCount += 1

        endTime = time.time()
        spendTime = endTime - startTime

        time.sleep(max(self.__duration - spendTime, 0))