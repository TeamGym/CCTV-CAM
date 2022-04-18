class Motion:
    def __init__(self, timestamp, rms):
        self.__timestamp = timestamp
        self.__rms = rms

    def as_dict(self):
        return {
            'timestamp': self.timestamp,
            'rms': self.rms
        }

    @property
    def timestamp(self):
        return self.__timestamp

    @property
    def rms(self):
        return self.__rms
