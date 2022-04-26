import time
import os

from Thread import ThreadLoopRunner
from Video import VideoWriter

class ClipExporter(ThreadLoopRunner):
    def __init__(self, prefix, fourcc, extension, width, height, fps, clipLength, videoBuffer):
        super().__init__(self.write, 1 / fps)

        self.__prefix = prefix
        self.__videoBuffer = videoBuffer

        self.__fourcc = fourcc
        self.__extension = extension
        self.__width = width
        self.__height = height
        self.__fps = fps

        self.__clipLength = clipLength
        self.__currentClipLength = 0

        self.__lastTime = time.time()

        self.__writer = VideoWriter()
        self.__makeNewClip()

    def __getFileName(self):
        return "{}{}.{}".format(
            self.__prefix,
            time.strftime("%Y-%m-%d/%H_%M_%S", time.localtime()),
            self.__extension)

    def __makeNewClip(self):
        self.__currentClipLength = 0

        os.makedirs(self.__prefix + time.strftime("%Y-%m-%d"), exist_ok=True)

        self.__writer.close()
        self.__writer.openFile(
            fileName=self.__getFileName(),
            fourcc=self.__fourcc,
            width=self.__width,
            height=self.__height,
            fps=self.__fps)

    def write(self):
        currentTime = time.time()
        self.__currentClipLength += currentTime - self.__lastTime
        self.__lastTime = currentTime

        if self.__currentClipLength >= self.__clipLength:
            self.__makeNewClip()

            print("[ClipExporter]: Saved current clip.")

        while self.__videoBuffer.size > 0:
            frame = self.__videoBuffer.pop()
            self.__writer.write(frame.data)
