import configparser

from Config.Config import Config

class DetectorConfig(Config):
    def __init__(self,
                 label : str = "",
                 config : str = "",
                 weights : str = "",
                 confidenceThreshold : float = 0.0):
        super().__init__()

        self.label = label
        self.config = config
        self.weights = weights
        self.confidenceThreshold = confidenceThreshold

    def load(self, filePath):
        config = configparser.ConfigParser()
        config.read(filePath)

        sections = config.sections()
        
        if not 'File' in sections:
            print("[DetectorConfig::load]: invalid config file. ('File' section doesn't exist.)")

        if not 'Parameter' in sections:
            print("[DetectorConfig::load]: invalid config file. ('Parameter' section doesn't exist.)")

        self.label = config['File']['label']
        self.config = config['File']['config']
        self.weights = config['File']['weights']

        self.confidenceThreshold = float(config['Parameter']['confidenceThreshold'])
