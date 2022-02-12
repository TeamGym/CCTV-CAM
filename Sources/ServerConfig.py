import configparser

from Config import Config
from CameraConfig import CameraConfig

class ServerConfig(Config):
    def __init__(self,
                 service : str = "3002",
                 mountpoint : str = '/webcam',
                 cameraConfig : CameraConfig = None):
        super().__init__()
        
        self.service = service
        self.mountpoint = mountpoint

        self.cameraConfig = cameraConfig

    def loadFromConfigFile(self, filePath):
        config = configparser.ConfigParser()
        config.read(filePath)

        sections = config.sections()
        
        if not 'RTSP' in sections:
            print("[CameraInfo::loadFromConfigFile]: invalid config file. ('RTSP' section doesn't exist.)")

        if not 'Camera' in sections:
            print("[CameraInfo::loadFromConfigFile]: invalid config file. ('Camera' section doesn't exist.)")

        self.service = config['RTSP']['service']
        self.mountpoint = config['RTSP']['mountpoint']

        cameraConfigPath = config['Camera']['configpath']

        self.cameraConfig = CameraConfig()
        self.cameraConfig.loadFromConfigFile(cameraConfigPath)

        if 'TCP' in sections:
            self.host = config['TCP']['host']
            self.port = int(config['TCP']['port'])
