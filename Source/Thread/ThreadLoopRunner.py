import time
from threading import Thread

class ThreadLoopRunner(Thread):
    def __init__(self, func, minInterval=0):
        super().__init__()

        self.__func = func

        self.__isRunning = False
        self.__minInterval = minInterval

    @property
    def func(self):
        return self.__func

    @property
    def isRunning(self):
        return self.__isRunning

    @isRunning.setter
    def isRunning(self, value):
        assert isinstance(value, bool)

        self.__isRunning = value

    @property
    def minInterval(self):
        return self.__minInterval

    @minInterval.setter
    def minInterval(self, value):
        self.__minInterval = value

    def run(self):
        self.isRunning = True
        while self.isRunning:
            startTime = time.time()

            self.__func()

            endTime = time.time()
            elapsedTime = endTime - startTime

            time.sleep(max(self.__minInterval - elapsedTime, 0))
