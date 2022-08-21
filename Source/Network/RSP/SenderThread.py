import logging
import socket
from threading import Thread
from queue import Queue
from collections import deque

from .Request import Request

l = logging.getLogger(__name__)
class SenderThread(Thread):
    def __init__(self, sock, onDisconnected):
        super().__init__()
        self.__sock = sock
        self.__onDisconnected = onDisconnected
        self.__sendMessageQueue = Queue()
        self.__sentRequestDict = {}

    @property
    def sendMessageQueue(self):
        return self.__sendMessageQueue

    @property
    def sentRequestDict(self):
        return self.__sentRequestDict

    def run(self):
        while True:
            message = self.__sendMessageQueue.get()
            if message is None:
                break
            messageString = message.getMessageString()
            l.debug('send message: \n{}'.format(messageString))

            try:
                self.__sock.sendall(messageString.encode('utf-8'))
            except BrokenPipeError:
                self.__onDisconnected()
                return

            if isinstance(message, Request):
                self.__sentRequestDict[message.sequence] = message
