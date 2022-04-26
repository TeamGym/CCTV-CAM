import time

from Thread import ThreadLoopRunner

class ObjectAlerter(ThreadLoopRunner):
    def __init__(self, interval, targets, cooldown, detectionBuffer, engine):
        super().__init__(self.alert, interval)

        self.__engine = engine
        self.__detectionBuffer = detectionBuffer

        self.__targets = targets
        self.__cooldown = cooldown

        self.__currentCooldown = 0
        self.__lastTime = time.time()

    def alert(self):
        currentTime = time.time()
        self.__currentCooldown -= currentTime - self.__lastTime

        while self.__detectionBuffer.size:
            detection = self.__detectionBuffer.pop()

            if self.__currentCooldown > 0:
                continue

            for box in detection.boxes:
                if box.label in self.__targets:
                    self.__engine.putMessage("{} Object Detected.".format(box.label))
                    self.__currentCooldown = self.__cooldown

        self.__lastTime = currentTime
