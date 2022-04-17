import time

import cv2
import numpy as np

from Core.Frame import Frame
from Core.Buffer import Buffer

class MotionDetector:
    def __init__(self, config, videoBuffer, outputBuffer, renderBuffer):
        self.__videoBuffer = videoBuffer
        self.__outputBuffer = outputBuffer
        self.__renderBuffer = renderBuffer

        self.__referenceFrame = None

        self.__latestFrame = None
        self.__latestFrameCount = 0
        self.__latestFrameRMSSum = 0

        self.__frameCount = 0

        self.__targetFPS = config.detector.motion.targetFPS
        self.__targetDuration = 1 / self.__targetFPS

        self.__updateInterval = config.detector.motion.updateInterval
        self.__RMSThreshold = config.detector.motion.threshold

    def detect(self):
        if self.__videoBuffer.size == 0:
            time.sleep(self.__targetDuration)
            return

        startTime = time.time()

        frame = self.__videoBuffer.tail()
        timestamp = frame.timestamp
        image = frame.data

        blurredImage = cv2.GaussianBlur(image, (7, 7), 0)

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

        if self.__latestFrameCount % self.__updateInterval == 0:
            if self.__latestFrameRMSSum <= self.__RMSThreshold * self.__updateInterval:
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

        _, diffThreshold = cv2.threshold(referenceDiff, 20, 255, cv2.THRESH_BINARY)

        mask = cv2.dilate(diffThreshold, (5, 5), iterations=2)
        mask = cv2.cvtColor(diffThreshold, cv2.COLOR_GRAY2RGB)

        maskedImage = cv2.bitwise_and(image, mask)
        maskedFrame = Frame(timestamp, maskedImage)

        self.__renderBuffer.push(maskedFrame)

        self.__latestFrameCount += 1
        self.__frameCount += 1

        endTime = time.time()
        elapsedTime = endTime - startTime

        if self.__targetDuration > elapsedTime:
            time.sleep(self.__targetDuration - elapsedTime)
