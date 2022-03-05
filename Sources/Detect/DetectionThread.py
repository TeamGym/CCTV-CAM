from threading import Thread

from Detect.Detector import Detector

class DetectionThread(Thread):
    def __init__(self, detector):
        super().__init__()

        self.detector = detector

    def run(self):
        while True:
            self.detector.detect()
