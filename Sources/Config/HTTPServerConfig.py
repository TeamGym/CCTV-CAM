from Config.Config import Config

class HTTPServerConfig(Config):
    def __init__(self,
                 url : str = ""):
        super().__init__()

        self.__url = url

    @property
    def url(self):
        return self.__url

    @url.setter
    def url(self, value):
        self.__url = value
