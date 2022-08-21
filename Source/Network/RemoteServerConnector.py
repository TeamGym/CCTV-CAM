import time
import sys
import socket
import json
import random

from Thread import ThreadRunner
from Network import VideoStreamer
from Network import AudioStreamer
from Network import AudioPlayer
from Network.RSP import RspConnection, Request, Response, Stream, EndpointType
from Network.RSP.stream_data import DetectionResult

class RemoteServerConnector(ThreadRunner):
    def __init__(self, host, port, videoWidth, videoHeight, videoFramerate, cameraId, connectionHolder,
                 videoBuffer, objectBuffer, motionBuffer, commandQueue, ID):
        super().__init__(func=self.communicate_automatically)

        self.__id = ID

        self.__host = host
        self.__port = port

        self.__videoWidth = videoWidth
        self.__videoHeight = videoHeight
        self.__videoFramerate = videoFramerate
        self.__videoBuffer = videoBuffer

        self.__objectBuffer = objectBuffer
        self.__motionBuffer = motionBuffer
        self.__commandQueue = commandQueue

        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.__serverStatus = connectionHolder.getConnection("TCP")

        self.__minCooldown = 1
        self.__maxCooldown = 10
        self.__currentCooldown = 1

        self.__latestTimestamp = 0

        self.__rspConnection = None
        self.__resetSequenceNumber()

        self.__videoStreamer = None
        self.__audioStreamer = None

        self.__videoOut = -1
        self.__audioOut = -1
        self.__outChannel = -1

        self.__audioPlayer = AudioPlayer(51001)
        self.__audioPlayer.start()

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
        if self.__outChannel < 0:
            return

        data = DetectionResult(
                timestamp=int(detection.timestamp * 1e9),
                boxes=[])

        for box in detection.boxes:
            data.boxes.append(DetectionResult.DetectionBox(
                left=box.x,
                right=box.x + box.width,
                top=box.y,
                bottom=box.y + box.height,
                confidence=box.confidence,
                classID=box.classID,
                label=box.label))

        self.__rspConnection.sendStream(Stream(
            channel=self.__outChannel,
            streamType=Stream.Type.DETECTION_RESULT,
            data=data))

    def connect(self):
        while True:
            self.__serverStatus.setTryingConnect()
            try:
                try:
                    self.__socket.close()
                except:
                    pass
                self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

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

        self.__rspConnection.addEventHandler('Disconnected', lambda connection: self.connect())
        self.__rspConnection.start()

        self.__rspConnection.sendRequest(Request(
            method=Request.Method.GET_INFO,
            onResponseCallback=self.__onGetInfo
        ))

    def __onGetInfo(self, response):
        ID = self.__id

        camList = [int(i) for i in response.getProperty('CamList').split(',')]
        method = Request.Method.GET_INFO,

        assert ID in camList

        audioIn = response.getProperty('Cam{}-AudioInPort'.format(ID))
        inChannel = response.getProperty('Cam{}-InChannel'.format(ID))

        self.__videoOut = int(response.getProperty('Cam{}-VideoPort'.format(ID)))
        self.__audioOut = int(response.getProperty('Cam{}-AudioOutPort'.format(ID)))
        self.__outChannel = int(response.getProperty('Cam{}-OutChannel'.format(ID)))

        if self.__audioStreamer is None:
            self.__audioStreamer = AudioStreamer(self.__host, self.__audioOut)
            self.__audioStreamer.start()

        if self.__videoStreamer is None:
            self.__videoStreamer = VideoStreamer(
                width=self.__videoWidth,
                height=self.__videoHeight,
                fps=self.__videoFramerate,
                host=self.__host,
                port=self.__videoOut,
                videoBuffer=self.__videoBuffer)
            self.__videoStreamer.start()


        self.__rspConnection.sendRequest(Request(
            method=Request.Method.JOIN,
            properties={'Type': 'UDP',
                        'Tunnel': audioIn,
                        'Listen': '51001'},
            onResponseCallback=lambda response : self.__onJoinedAudio(response, 51001)
        ))

        self.__rspConnection.sendRequest(Request(
            method=Request.Method.JOIN,
            properties={'Type': 'STREAM',
                        'Tunnel': inChannel,
                        'Listen': '0'},
            onResponseCallback=lambda response : self.__onJoinedStream(response)
        ))

    def __onJoinedAudio(self, response, port):
        pass

    def __onJoinedStream(self, response):
        pass

    def communicate(self):
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
