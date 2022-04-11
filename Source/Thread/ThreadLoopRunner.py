from threading import Thread

class ThreadLoopRunner(Thread):
    def __init__(self, func):
        super().__init__()

        self.__func = func
        self.__isRunning = True

    @property
    def func(self):
        return self.__func

    def isRunning(self):
        return self.__isRunning

    def setRunning(self, value):
        assert isinstance(value, bool)

        self.__isRunning = value

    def run(self):
        while self.isRunning():
            self.__func()
