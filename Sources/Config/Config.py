import configparser

class Config:
    def __init__(self):
        pass

    def __getitem__(self, key):
        return getattr(self, key)

    def __setitem__(self, key, value):
        return setattr(self, key, value)

    def load(self, filePath):
        config = configparser.ConfigParser()
        config.read(filePath)

        sections = config.sections()

        for section in sections:
            for key in config[section]:
                setattr(self, key, config[section][key])
                
