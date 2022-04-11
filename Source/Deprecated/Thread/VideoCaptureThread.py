from threading import Thread

from Capture.VideoCapture import VideoCapture

class VideoCaptureThread(Thread):
    def __init__(self,
                 capture : VideoCapture):
        super().__init__()

        self.capture = capture

    def run(self):
        while True:
            self.capture.read()
