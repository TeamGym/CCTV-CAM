import json

class JSONConfig:
    def __init__(self, filePath=""):
        if len(filePath) == 0:
            return

        self.load(filePath)

    def __getitem__(self, key):
        return getattr(self, key)

    def __setitem__(self, key, value):
        return setattr(self, key, value)

    def load(self, filePath):
        with open(filePath, "r") as configFile:
            parserResult = json.load(configFile)

            self.__dict__ = parserResult
