import time
import sys
import socket
import json
import random

from Thread import ThreadRunner
from Network.RSP import RspConnection, Request, Response, EndpointType

class RemoteServerConnector(ThreadRunner):
    def __init__(self, host, port, videoWidth, videoHeight, cameraId, connectionHolder,
                 objectBuffer, motionBuffer, commandQueue):
        super().__init__(func=self.communicate_automatically)

        self.__host = host
        self.__port = port

        self.__videoWidth = videoWidth
        self.__videoHeight = videoHeight

        self.__objectBuffer = objectBuffer
        self.__motionBuffer = motionBuffer
        self.__commandQueue = commandQueue

        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__socket.settimeout(10)

        self.__serverStatus = connectionHolder.getConnection("TCP")

        self.__minCooldown = 1
        self.__maxCooldown = 10
        self.__currentCooldown = 1

        self.__latestTimestamp = 0

        self.__rspConnection = None
        self.__resetSequenceNumber()

    @property
    def host(self):
        return self.__host

    @property
    def port(self):
        return self.__port

    @property
    def socket(self):
        return self.__socket

    def __resetSequenceNumber(self):
        self.__sequenceNumber = random.randint(0, 2147483647)

    def __send(self, data):
        self.__socket.sendall(data)

    def __waitUntilCooldown(self):
        time.sleep(self.__currentCooldown)

    def __resetCooldown(self):
        self.__currentCooldown = self.__minCooldown

    def __increaseCooldown(self):
        self.__currentCooldown = min(self.__currentCooldown + 1, self.__maxCooldown)

    def __sendObject(self, detection):
        stream = "S{} 1\n".format(self.__port)

        stream += "{}\n".format(int(detection.timestamp))

        for box in detection.boxes:
            stream += "{},{},{},{},{},{},{}\n".format(
                box.x,
                box.x + box.width,
                box.y,
                box.y + box.height,
                box.confidence,
                box.classID,
                box.label)

        self.__rspConnection.sendStream(stream)

    def connect(self):
        while True:
            self.__serverStatus.setTryingConnect()
            try:
                if self.__socket.connect_ex((self.__host, self.__port)):
                    print("[RemoteServerConnector]: Can't connect TCP server, wait {} second."
                          .format(self.__currentCooldown))

                    self.__waitUntilCooldown()
                    self.__increaseCooldown()
                else:
                    break
            except Exception as e:
                print("[RemoteServerConnector]: Can't connect TCP server, wait {} seconds."
                      .format(self.__currentCooldown))
                self.__waitUntilCooldown()
                self.__increaseCooldown()

        self.__serverStatus.setConnected()
        self.__resetCooldown()

        print("[RemoteServerConnector]: Connected successfully.")

        self.__rspConnection = RspConnection(
            endpointType=EndpointType.CAM,
            sock=self.__socket)

        self.__rspConnection.addEventHandler('Disconnected', self.__connect)
        self.__rspConnection.start()

    def communicate(self):
        print("[RemoteServerConnector]: Attempt to send CCTV info.")

        while True:
            if self.__objectBuffer.size <= 0:
                time.sleep(1 / 30.0)
                continue

            detection = self.__objectBuffer.tail()
            timestamp = detection.timestamp

            if timestamp <= self.__latestTimestamp:
                time.sleep(0.1)
                continue

            self.__sendObject(detection)

            self.__latestTimestamp = timestamp

    def communicate_automatically(self):
        self.__serverStatus.setUnconnected()
        self.connect()

        while True:
            try:
                self.communicate()
            except OSError as e:
                print("[RemoteServerConnector]: Unexpected error. Attempt to re-connect.(Error: {})".format(e), file=sys.stderr)

                self.__serverStatus.setUnconnected()
                self.connect()
