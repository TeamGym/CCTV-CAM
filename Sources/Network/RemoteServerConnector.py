import time
import sys
import socket
import json

from numpyencoder import NumpyEncoder

from Core.Buffer import Buffer
from Detect.DetectionBox import DetectionBox
from Detect.Detection import Detection

class RemoteServerConnector:
    def __init__(self, context):

        self.__context = context

        self.__host = context.tcpHost
        self.__port = context.tcpPort

        self.__videoWidth = context.width
        self.__videoHeight = context.height

        self.__detectionBuffer = context.detectionBuffer
        self.__commandQueue = context.commandQueue

        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__socket.settimeout(10)

        self.__latestTimestamp = 0

    @property
    def host(self):
        return self.__host

    @property
    def port(self):
        return self.__port

    @property
    def socket(self):
        return self.__socket

    def connect(self):
        while True:
            self.__context.tcpStatus = "Connecting"
            try:
                if self.__socket.connect_ex((self.__host, self.__port)):
                    print("[RemoteServerConnector]: Can't connect TCP server, wait 3 second.")
                    time.sleep(3)
                else:
                    break
            except:
                print("[RemoteServerConnector]: Can't connect TCP server, wait 3 second.")
                time.sleep(3)

        print("[RemoteServerConnector]: Connected successfully.")

    def communicate(self):
        cctvInfo = {
            "cam_id": 0,
            "mode": 1,
            "video_width": self.__videoWidth,
            "video_height": self.__videoHeight
        }
        cctvInfo = json.dumps(cctvInfo)
        cctvInfo = cctvInfo.encode('utf-8')

        print("[RemoteServerConnector]:  Attempt to send CCTV info.")

        self.__socket.sendall(cctvInfo)

        self.__context.tcpStatus = "Connected"

        while True:
            if self.__detectionBuffer.size <= 0:
                time.sleep(0.1)
                continue

            detection = self.__detectionBuffer.tail()
            timestamp = detection.timestamp

            if timestamp <= self.__latestTimestamp:
                time.sleep(0.1)
                continue

            self.__latestTimestamp = timestamp

            #print("[RemoteServerConnector]: Attempt to send detection data.(boxes: {})"
            #      .format(len(detection.boxes)))

            data = {
                "timestamp": detection.timestamp / 1e6,
                "boxes": [box.as_dict() for box in detection.boxes]
            }
            data = json.dumps(data, cls=NumpyEncoder)
            data = data.replace(" ", "")
            data = data.encode('utf-8')

            self.__socket.send(data)

    def communicate_automatically(self):
        self.__context.tcpStatus = "Unconnected"
        self.connect()

        while True:
            try:
                self.communicate()
            except OSError as e:
                print("[RemoteServerConnector]: Unexpected error. Attempt to re-connect.(Error: {})".format(e), file=sys.stderr)

                self.__context.tcpStatus = "Unconnected"
                self.connect()
