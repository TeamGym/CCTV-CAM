import os
import sys

import configparser

from Config.StreamingServerConfig import StreamingServerConfig
from Config.DetectionServerConfig import DetectionServerConfig
from Config.HTTPServerConfig import HTTPServerConfig

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
        
        if not 'Detection' in sections:
            print("[ServerConfigLoader::Load]: invalid config file. ('DetectionServer' section doesn't exist.)")
            sys.exit(1)

        if not 'Streaming' in sections:
            print("[ServerConfigLoader::Load]: invalid config file. ('StreamingServer' section doesn't exist.)")
            sys.exit(1)
            
        if not 'HTTP' in sections:
            print("[ServerConfigLoader::Load]: invalid config file. ('HTTPServer' section doesn't exist.)")
            sys.exit(1)

        self.detection = DetectionServerConfig()
        self.streaming = StreamingServerConfig()
        self.http = HTTPServerConfig()

        self.detection.host = config['Detection']['host']
        self.detection.port = int(config['Detection']['port'])

        self.streaming.host = config['Streaming']['host']
        self.streaming.port = int(config['Streaming']['port'])

        self.http.url = config['HTTP']['url']
