import json

class JSON:
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
                subJson = JSON()
                subJson.loadDict(value)
                setattr(self, name, subJson)

    def loadFile(self, filePath):
        with open(filePath, "r") as file:
            self.__dict__ = json.load(file)

            self.__loadRecursively()

    def loadString(self, jsonStr):
        self.__dict__ = json.loads(jsonStr)

        self.__loadRecursively()

    def loadDict(self, dictionary):
        self.__dict__ = dictionary

        self.__loadRecursively()
