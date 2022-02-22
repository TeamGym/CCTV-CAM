import time
import socket
import json

from Core.Buffer import Buffer
from Detect.DetectionBox import DetectionBox
from Detect.DetectionResult import DetectionResult

class DetectionSender:
    def __init__(self,
                 host : str,
                 port : int,
                 detectionResultBuffer : Buffer):
        
        self.host = host
        self.port = port

        self.detectionResultBuffer = detectionResultBuffer

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)        
        self.socket.settimeout(10)
        
        self.latestTimestamp = 0

    def connect(self):
        while True:
            try:
                if self.socket.connect_ex((self.host, self.port)):
                    print("[DetectionSender]: Can't connect server, wait 3 second.")
                    time.sleep(3)
                else:
                    break
            except:
                print("[DetectionSender]: Can't connect server, wait 3 second.")
                time.sleep(3)
                continue

    def start(self):
        cctvInfo = {
            "cam_id": 0,
            "mode": 1,
        }
        cctvInfo = json.dumps(cctvInfo)
        cctvInfo = cctvInfo.encode('utf-8')

        self.socket.sendall(cctvInfo)

        while True:
            if self.detectionResultBuffer.size <= 0:
                continue

            detectionResult = self.detectionResultBuffer.tail()            
            timestamp = detectionResult.timestamp            

            if timestamp <= self.latestTimestamp:
                continue
            
            self.latestTimestamp = timestamp

            detectionResult = json.dumps(detectionResult.as_dict())
            detectionResult = detectionResult.encode('utf-8')
            
            self.socket.send(detectionResult)
            
            

            

