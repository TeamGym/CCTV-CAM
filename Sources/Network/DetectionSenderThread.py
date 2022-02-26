from threading import Thread

from Core.Buffer import Buffer
from Config.DetectionServerConfig import DetectionServerConfig
from Config.HTTPServerConfig import HTTPServerConfig
from Config.CameraConfig import CameraConfig

from Detect.DetectionResult import DetectionResult
from Network.DetectionSender import DetectionSender

import sys
import socket
import json

class DetectionSenderThread(Thread):
    def __init__(self,
                 detectionServerConfig : DetectionServerConfig,
                 httpServerConfig : HTTPServerConfig,
                 cameraConfig : CameraConfig,
                 detectionResultBuffer : Buffer):
        super().__init__()

        self.detectionResultBuffer = detectionResultBuffer

        host = detectionServerConfig.host
        port = detectionServerConfig.port

        url = httpServerConfig.url

        videoWidth = cameraConfig.width
        videoHeight = cameraConfig.height

        self.sender = DetectionSender(host, port, url, videoWidth, videoHeight, detectionResultBuffer)

    def run(self):
        self.sender.communicate_automatically()
