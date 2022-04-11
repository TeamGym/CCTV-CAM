from threading import Thread

from Network.RemoteServerConnector import RemoteServerConnector

class RemoteServerConnectorThread(Thread):
    def __init__(self, connector : RemoteServerConnector):
        super().__init__()

        self.connector = connector

    def run(self):
        self.connector.communicate_automatically()
