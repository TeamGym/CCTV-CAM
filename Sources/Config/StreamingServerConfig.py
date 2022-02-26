from Config.Config import Config

class StreamingServerConfig(Config):
    def __init__(self,
                 host : str = "127.0.0.1",
                 port : int = "50001"):
        super().__init__()

        self.__host = host
        self.__port = port

    @property
    def host(self):
        return self.__host

    @host.setter
    def host(self, value):
        self.__host = value

    @property
    def port(self):
        return self.__port

    @port.setter
    def port(self, value):
        self.__port = value
