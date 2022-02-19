from Config import Config

class StreamingServerConfig(Config):
    def __init__(self,
                 service : str = "5001",
                 mountpoint : str = '/stream'):
        super().__init__()

        self.__service = service
        self.__mountpoint = mountpoint

    @property
    def service(self):
        return self.__service

    @service.setter
    def service(self, value):
        self.__service = value

    @property
    def mountpoint(self):
        return self.__mountpoint

    @mountpoint.setter
    def mountpoint(self, value):
        self.__mountpoint = value
