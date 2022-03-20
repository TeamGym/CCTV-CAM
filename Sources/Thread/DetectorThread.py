from threading import Thread

class DetectorThread(Thread):
    def __init__(self, detector):
        super().__init__()

        self.detector = detector

    def run(self):
        while True:
            self.detector.detect()
