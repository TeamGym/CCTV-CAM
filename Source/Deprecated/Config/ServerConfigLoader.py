import os
import sys

import configparser

from Config.RTSPServerConfig import RTSPServerConfig
from Config.TCPServerConfig import TCPServerConfig

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

        if not 'TCP' in sections:
            print("[ServerConfigLoader::Load]: invalid config file. ('TCP' section doesn't exist.)")
            sys.exit(1)

        if not 'RTSP' in sections:
            print("[ServerConfigLoader::Load]: invalid config file. ('RTSP' section doesn't exist.)")
            sys.exit(1)


        self.tcp = TCPServerConfig()
        self.rtsp = RTSPServerConfig()


        self.tcp.host = config['TCP']['host']
        self.tcp.port = int(config['TCP']['port'])

        self.rtsp.location = config['RTSP']['location']
