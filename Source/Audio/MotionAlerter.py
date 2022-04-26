import time

from Thread import ThreadLoopRunner

class MotionAlerter(ThreadLoopRunner):
    def __init__(self, config, detectionBuffer, engine):
        super().__init__(self.alert, config.audio.alert.motion.minInterval)

        self.__engine = engine
        self.__detectionBuffer = detectionBuffer

        self.__cooldown = config.audio.alert.motion.cooldown

        self.__currentCooldown = 0
        self.__lastTime = time.time()

    def alert(self):
        currentTime = time.time()
        self.__currentCooldown -= currentTime - self.__lastTime

        while self.__detectionBuffer.size:
            detection = self.__detectionBuffer.pop()

            if self.__currentCooldown <= 0:
                self.__engine.putMessage("Motion Detected.")
                self.__currentCooldown = self.__cooldown

        self.__lastTime = currentTime
