import json

class JSONConfig:
    def __init__(self):
        pass

    def __getitem__(self, key):
        return getattr(self, key)

    def __setitem__(self, key, value):
        return setattr(self, key, value)

    def __loadRecursively(self):
        for name in self.__dict__:
            value = getattr(self, name)
            if isinstance(value, dict):
                subConfig = JSONConfig()
                subConfig.loadDict(value)
                setattr(self, name, subConfig)

    def loadFile(self, filePath):
        with open(filePath, "r") as configFile:
            self.__dict__ = json.load(configFile)

            self.__loadRecursively()

    def loadString(self, jsonStr):
        self.__dict__ = json.loads(jsonStr)

        self.__loadRecursively()

    def loadDict(self, dictionary):
        self.__dict__ = dictionary

        self.__loadRecursively()
