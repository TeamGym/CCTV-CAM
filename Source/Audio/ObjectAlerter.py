import time

from Thread.ThreadLoopRunner import ThreadLoopRunner

class ObjectAlerter(ThreadLoopRunner):
    def __init__(self, config, detectionBuffer, engine):
        super().__init__(self.alert, config.audio.alert.object.minInterval)

        self.__engine = engine
        self.__detectionBuffer = detectionBuffer
        self.__targets = config.audio.alert.object.targets

        print(self.__targets)

    def alert(self):
        while self.__detectionBuffer.size:
            detection = self.__detectionBuffer.pop()

            for box in detection.boxes:
                if box.label in self.__targets:
                    self.__engine.putMessage("{} Object Detected.".format(box.label))
