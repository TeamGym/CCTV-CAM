from Config import Config

class DetectionServerConfig(Config):
    def __init__(self,
                 host : str = "0.0.0.0",
                 port : int = "5000"):
        super().__init__()

        self.__host = host
        self.__port = port

    @property
    def host(self):
        return self.__host

    @host.setter
    def host(self, value):
        self.__host = value
