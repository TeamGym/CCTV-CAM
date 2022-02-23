from threading import Thread

from Core.Buffer import Buffer
from Config.DetectionServerConfig import DetectionServerConfig
from Config.CameraConfig import CameraConfig

from Detect.DetectionResult import DetectionResult
from Stream.DetectionSender import DetectionSender

import sys
import socket
import json

class DetectionSenderThread(Thread):
    def __init__(self,
                 serverConfig : DetectionServerConfig,
                 cameraConfig : CameraConfig,
                 detectionResultBuffer : Buffer):
        super().__init__()

        self.detectionResultBuffer = detectionResultBuffer

        host = serverConfig.host
        port = serverConfig.port

        videoWidth = cameraConfig.width
        videoHeight = cameraConfig.height

        self.sender = DetectionSender(host, port, videoWidth, videoHeight, detectionResultBuffer)

    def run(self):
        self.sender.communicate_automatically()
