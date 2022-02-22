from threading import Thread

from Core.Buffer import Buffer
from Config.DetectionServerConfig import DetectionServerConfig

from Detect.DetectionResult import DetectionResult
from Stream.DetectionSender import DetectionSender

import socket
import json

class DetectionSenderThread(Thread):
    def __init__(self,
                 serverConfig : DetectionServerConfig,
                 detectionResultBuffer : Buffer):
        super().__init__()

        self.detectionResultBuffer = detectionResultBuffer

        host = serverConfig.host
        port = serverConfig.port

        self.sender = DetectionSender(host, port)

    def run(self):
        self.sender.connect()
        self.sender.start()

