from Config.Config import Config

class StreamingServerConfig(Config):
    def __init__(self,
                 location : str = ""):
        super().__init__()

        self.__location = location

    @property
    def location(self):
        return self.__location

    @location.setter
    def location(self, value):
        self.__location = value
