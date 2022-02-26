import time
import sys
import socket
import json
import requests

from numpyencoder import NumpyEncoder

from Core.Buffer import Buffer
from Detect.DetectionBox import DetectionBox
from Detect.DetectionResult import DetectionResult

class DetectionSender:
    def __init__(self,
                 host : str,
                 port : int,
                 url : str,
                 videoWidth : int,
                 videoHeight : int,
                 detectionResultBuffer : Buffer):
        
        self.host = host
        self.port = port

        self.url = url

        self.videoWidth = videoWidth
        self.videoHeight = videoHeight

        self.detectionResultBuffer = detectionResultBuffer

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)        
        self.socket.settimeout(10)
        
        self.latestTimestamp = 0

    def connect(self):
        statusCode = ""
        while True:
            try:
                response = requests.post(self.url, "record")
                statusCode = response.status_code

                if statusCode.startsWith("2"):
                    break

                print("[DetectionSender]: Can't connect HTTP server, wait 3 second.")
                time.sleep(3)
            except:
                print("[DetectionSender]: Can't connect HTTP server, wait 3 second.")
                time.sleep(3)
            
        while True:
            try:
                if self.socket.connect_ex((self.host, self.port)):
                    print("[DetectionSender]: Can't connect TCP server, wait 3 second.")
                    time.sleep(3)
                else:
                    break
            except:
                print("[DetectionSender]: Can't connect TCP server, wait 3 second.")
                time.sleep(3)

        print("[DetectionSender]: Connected successfully.")

    def communicate(self):
        cctvInfo = {
            "cam_id": 0,
            "mode": 1,
            "video_width": self.videoWidth,
            "video_height": self.videoHeight
        }
        cctvInfo = json.dumps(cctvInfo)
        cctvInfo = cctvInfo.encode('utf-8')

        print("[DetectionSender]:  Attempt to send CCTV info.")

        self.socket.sendall(cctvInfo)

        while True:        
            if self.detectionResultBuffer.size <= 0:
                time.sleep(0.1)
                continue

            detectionResult = self.detectionResultBuffer.tail()            
            timestamp = detectionResult.timestamp

            if timestamp <= self.latestTimestamp:
                time.sleep(0.1)
                continue

            self.latestTimestamp = timestamp

            #print("[DetectionSender]: Attempt to send detection data.(boxes: {})"
            #      .format(len(detectionResult.boxes)))

            data = {
                "timestamp": detectionResult.timestamp / 1e6,
                "boxes": [box.as_dict() for box in detectionResult.boxes]
            }
            data = json.dumps(data, cls=NumpyEncoder)
            data = data.replace(" ", "")
            data = data.encode('utf-8')

            self.socket.send(data)

    def communicate_automatically(self):
         self.connect()
         
         while True:
            try:
                self.communicate()
            except OSError as e:
                print("[DetectionSenderThread]: Unexpected error. Attempt to re-connect.(Error: {})".format(e), file=sys.stderr)
                self.connect()


            

