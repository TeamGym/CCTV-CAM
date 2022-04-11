from threading import Thread

class ThreadRunner(Thread):
    def __init__(self, func):
        super().__init__()

        self.__func = func

    @property
    def func(self):
        return self.__func

    def run(self):
        self.__func()
