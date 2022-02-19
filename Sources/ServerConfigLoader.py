import os
import sys

import configparser

from StreamingServerConfig import StreamingServerConfig
from DetectionServerConfig import DetectionServerConfig

class ServerConfigLoader:
    def __init__(self, filePath : str = ""):
        if filePath:
            self.load(filePath)

    def load(self, filePath):
        if not os.path.isfile(filePath):
            print("[ServerConfigLoader::load]: {} is not file.".format(filePath))
            sys.exit(1)
                  
        config = configparser.ConfigParser()
        config.read(filePath)

        sections = config.sections()
        
        if not 'DetectionServer' in sections:
            print("[ServerConfigLoader::Load]: invalid config file. ('DetectionServer' section doesn't exist.)")
            sys.exit(1)

        if not 'StreamingServer' in sections:
            print("[ServerConfigLoader::Load]: invalid config file. ('StreamingServer' section doesn't exist.)")
            sys.exit(1)

        self.detection = DetectionServerConfig()
        self.streaming = StreamingServerConfig()

        self.detection.host = config['DetectionServer']['host']
        self.detection.port = int(config['DetectionServer']['port'])

        self.streaming.service = config['StreamingServer']['service']
        self.streaming.mountpoint = config['StreamingServer']['mountpoint']
