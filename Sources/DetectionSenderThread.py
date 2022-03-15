from threading import Thread

from Network.DetectionSender import DetectionSender

class DetectionSenderThread(Thread):
    def __init__(self, sender : DetectionSender):
        super().__init__()
        
        self.sender = sender

    def run(self):
        self.sender.communicate_automatically()
