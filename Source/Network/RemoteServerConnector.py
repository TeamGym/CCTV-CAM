import time
import sys
import socket
import json

from numpyencoder import NumpyEncoder

from Detect.DetectionBox import DetectionBox
from Detect.Detection import Detection

from Thread.ThreadRunner import ThreadRunner

class RemoteServerConnector(ThreadRunner):
    def __init__(self, config, connectionHolder,
                 objectBuffer, motionBuffer, commandQueue):
        super().__init__(func=self.communicate_automatically)

        self.__host = config.network.tcp.host
        self.__port = config.network.tcp.port

        self.__videoWidth = config.device.camera.width
        self.__videoHeight = config.device.camera.height

        self.__objectBuffer = objectBuffer
        self.__motionBuffer = motionBuffer
        self.__commandQueue = commandQueue

        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__socket.settimeout(10)

        self.__serverStatus = connectionHolder.getConnection("TCP")

        self.__minTimeout = 1
        self.__maxTimeout = 10
        self.__currentTimeout = 1

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
            self.__serverStatus.setTryingConnect()
            try:
                if self.__socket.connect_ex((self.__host, self.__port)):
                    print("[RemoteServerConnector]: Can't connect TCP server, wait {} second."
                          .format(self.__currentTimeout))
                    time.sleep(self.__currentTimeout)

                    self.__currentTimeout = min(self.__currentTimeout + 1, self.__maxTimeout)
                else:
                    break
            except:
                print("[RemoteServerConnector]: Can't connect TCP server, wait {} seconds."
                      .format(self.__currentTimeout))
                time.sleep(self.__currentTimeout)

                self.__currentTimeout = min(self.__currentTimeout + 1, self.__maxTimeout)

        self.__serverStatus.setConnected()
        self.__currentTimeout = self.__minTimeout

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

        self.__serverStatus.setConnected()

        while True:
            if self.__objectBuffer.size <= 0:
                time.sleep(1 / 30.0)
                continue

            detection = self.__objectBuffer.tail()
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
        self.__serverStatus.setUnconnected()
        self.connect()

        while True:
            try:
                self.communicate()
            except OSError as e:
                print("[RemoteServerConnector]: Unexpected error. Attempt to re-connect.(Error: {})".format(e), file=sys.stderr)

                self.__serverStatus.setUnconnectd()
                self.connect()
