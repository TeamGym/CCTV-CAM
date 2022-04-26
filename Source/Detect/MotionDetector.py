import time

import cv2
import numpy as np

from Core import Frame
from Detect import Motion
from Thread import ThreadLoopRunner

from Detect.Motion import Motion

class MotionDetector:
    def __init__(self, config, videoBuffer, outputBuffer, renderBuffer):
        self.__videoBuffer = videoBuffer
        self.__outputBuffer = outputBuffer
        self.__renderBuffer = renderBuffer

        self.__referenceFrame = None

        self.__latestFrame = None
        self.__latestFrameCount = 0
        self.__latestRMSSum = 0

        self.__frameCount = 0

        self.__targetFPS = config.detector.motion.targetFPS
        self.__targetDuration = 1 / self.__targetFPS

        self.__updateInterval = config.detector.motion.updateInterval
        self.__updateThresholdPerFrame = config.detector.motion.updateThreshold
        self.__motionThresholdPerFrame = config.detector.motion.motionThreshold
        self.__updateThreshold = self.__updateThresholdPerFrame * self.__updateInterval
        self.__motionThreshold = self.__motionThresholdPerFrame * self.__updateInterval

        self.__isDetected = False

    def __initialize(self, frame):
        if self.__referenceFrame is None:
            self.__referenceFrame = frame

        if self.__latestFrame is None:
            self.__latestFrame = frame

    def __getFrame(self):
        frame = self.__videoBuffer.pop()

        self.__videoBuffer.clear()
        return frame

    def __getDiff(self, image1, image2):
        return cv2.absdiff(image1, image2)

    def __getRMSFromDiff(self, diff):
        return np.sqrt(cv2.mean(cv2.pow(diff, power=2))[0])

    def __getMaskFromDiff(self, diff):
        _, diffThreshold = cv2.threshold(diff, 20, 255, cv2.THRESH_BINARY)

        mask = cv2.dilate(diffThreshold, (5, 5), iterations=2)
        mask = cv2.cvtColor(diffThreshold, cv2.COLOR_GRAY2RGB)

        return mask

    def __getRenderImage(self, image, mask):
        renderImage = cv2.bitwise_and(image, mask)
        (imageHeight, imageWidth, _) = renderImage.shape

        if self.__isDetected:
            cv2.putText(renderImage, "Motion Detected.",
                (0, imageHeight - 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (20, 20, 240), 2)

        return renderImage

    def __update(self, frame):
        if self.__latestFrameCount % self.__updateInterval == 0:
            self.__isDetected = self.__latestRMSSum >= self.__motionThreshold

            if self.__latestRMSSum <= self.__updateThreshold:
                self.__referenceFrame = frame

            if self.__isDetected:
                self.__outputBuffer.push(Motion(frame.timestamp, self.__latestRMSSum))

            self.__latestFrameCount = 0
            self.__latestRMSSum = 0

            self.__latestFrame = frame

        self.__latestFrameCount += 1
        self.__frameCount += 1

    def detect(self):
        if self.__videoBuffer.size == 0:
            return

        startTime = time.time()

        frame = self.__getFrame()
        (timestamp, image) = (frame.timestamp, frame.data)

        blurredImage = cv2.GaussianBlur(image, (7, 7), 0)

        grayImage = cv2.cvtColor(blurredImage, cv2.COLOR_BGR2GRAY)
        grayFrame = Frame(timestamp, grayImage)

        self.__initialize(grayFrame)

        referenceDiff = self.__getDiff(grayImage, self.__referenceFrame.data)
        referenceRMS = self.__getRMSFromDiff(referenceDiff)

        latestDiff = self.__getDiff(grayImage, self.__latestFrame.data)
        latestRMS = self.__getRMSFromDiff(latestDiff)

        self.__latestRMSSum += latestRMS
        self.__update(grayFrame)

        mask = self.__getMaskFromDiff(referenceDiff)

        renderImage = self.__getRenderImage(image, mask)
        renderFrame = Frame(timestamp, renderImage)

        self.__renderBuffer.push(renderFrame)
