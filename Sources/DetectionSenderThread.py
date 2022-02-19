from threading import Thread

from Core.Buffer import Buffer

from DetectionServerConfig import DetectionServerConfig
from DetectionResult import DetectionResult

import socket
import dill

class DetectionSenderThread(Thread):
    def __init__(self,
                 serverConfig : DetectionServerConfig,
                 detectionResultBuffer : Buffer):
        super().__init__()

        self.detectionResultBuffer = detectionResultBuffer

        self.host = serverConfig.host
        self.port = serverConfig.port

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        self.socket.bind((self.host, self.port))

        self.latestTimestamp = 0

    def run(self):
        while True:
            self.socket.listen()

            connection, address = self.socket.accept()
            print(connection, address)

            while True:
                if self.detectionResultBuffer.size <= 0:
                    continue

                detectionResult = self.detectionResultBuffer.tail()
                timestamp = detectionResult.timestamp

                if timestamp <= self.latestTimestamp:
                    continue

                data = dill.dumps(detectionResult)
                connection.send(data)

                self.latestTimestamp = detectionResult.timestamp

            connection.close()

        self.socket.shutdown(socket.SHUT_RDWR)
        self.socket.close()


