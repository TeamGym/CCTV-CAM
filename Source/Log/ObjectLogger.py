import time
import logging

from Thread import ThreadLoopRunner

class ObjectLogger(ThreadLoopRunner):
    def __init__(self, filePath, detectionBuffer):
        super().__init__(self.log, 1 / 30)

        self.__logger = logging.getLogger("Object")

        self.__fileHandler = logging.FileHandler(filePath)
        self.__formatter = logging.Formatter('[%(asctime)s] %(message)s')

        self.__logger.setLevel(level=logging.INFO)
        self.__fileHandler.setFormatter(self.__formatter)
        self.__logger.addHandler(self.__fileHandler)

        self.__detectionBuffer = detectionBuffer

    def log(self):
        while self.__detectionBuffer.size:
            detection = self.__detectionBuffer.pop()
            timestamp = detection.timestamp

            for box in detection.boxes:
                self.__logger.info("Object timestamp={}, x={}, y={}, width={}, height={}, "
                                   "confidence={}, classID={}, label={}".format(
                                       timestamp, box.x, box.y, box.width, box.height,
                                       box.confidence, box.classID, box.label))
