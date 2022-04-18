import time

from Thread.ThreadLoopRunner import ThreadLoopRunner

class MotionAlerter(ThreadLoopRunner):
    def __init__(self, config, detectionBuffer, engine):
        super().__init__(self.alert, config.audio.alert.motion.minInterval)

        self.__engine = engine
        self.__detectionBuffer = detectionBuffer

    def alert(self):
        while self.__detectionBuffer.size:
            detection = self.__detectionBuffer.pop()

            self.__engine.putMessage("Motion Detected.")
