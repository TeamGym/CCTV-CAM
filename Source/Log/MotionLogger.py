import time
import logging

from Thread.ThreadLoopRunner import ThreadLoopRunner

class MotionLogger(ThreadLoopRunner):
    def __init__(self, filePath, detectionBuffer):
        super().__init__(self.log, 1 / 30)

        self.__logger = logging.getLogger("Motion")

        self.__fileHandler = logging.FileHandler(filePath)
        self.__formatter = logging.Formatter('[%(asctime)s] %(message)s')

        self.__logger.setLevel(level=logging.INFO)
        self.__fileHandler.setFormatter(self.__formatter)
        self.__logger.addHandler(self.__fileHandler)

        self.__detectionBuffer = detectionBuffer

    def log(self):
        while self.__detectionBuffer.size:
            detection = self.__detectionBuffer.pop()
            self.__logger.info("Motion timestamp={}, rms={}".format(
                detection.timestamp, detection.rms))
