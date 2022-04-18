import time
import pyttsx3

from Thread.ThreadLoopRunner import ThreadLoopRunner
from queue import Queue

class TTSEngine(ThreadLoopRunner):
    def __init__(self):
        super().__init__(self.speakMessage)

        self.__engine = pyttsx3.init()
        self.__messageQueue = Queue()

    def putMessage(self, message):
        self.__messageQueue.put(message)

    def speakMessage(self):
        startTime = time.time()

        message = self.__messageQueue.get()
        self.__engine.say(message)
        self.__engine.runAndWait()
