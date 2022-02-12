import configparser

from Config import Config

class CameraConfig(Config):
    def __init__(self,
                 device : str = '/dev/video0',
                 width : int = 640,
                 height : int = 480,
                 fps : int = 30,
                 format : str = 'YUY2'):
        super().__init__()
        
        self.device = device
        self.width = width
        self.height = height
        self.fps = fps
        self.format = format

    def loadFromConfigFile(self, filePath):
        config = configparser.ConfigParser()
        config.read(filePath)

        sections = config.sections()
        
        if not 'Driver' in sections:
            print("[CameraConfig::loadFromConfigFile]: invalid config file. ('Driver' section doesn't exist.)")

        if not 'Input' in sections:
            print("[CameraConfig::loadFromConfigFile]: invalid config file. ('Input' section doesn't exist.)")

        self.device = config['Driver']['device']

        self.width = int(config['Input']['width'])
        self.height = int(config['Input']['height'])
        self.fps = int(config['Input']['fps'])
        self.format = config['Input']['format']
