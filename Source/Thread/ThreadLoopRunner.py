import time
from threading import Thread

class ThreadLoopRunner(Thread):
    def __init__(self, func, interval=0):
        super().__init__()

        self.__func = func

        self.__isRunning = False
        self.__interval = interval

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
    def interval(self):
        return self.__interval

    @interval.setter
    def interval(self, value):
        self.__interval = value

    def run(self):
        self.isRunning = True
        while self.isRunning:
            startTime = time.time()

            self.__func()

            endTime = time.time()
            elapsedTime = endTime - startTime

            time.sleep(max(self.__interval - elapsedTime, 0))
