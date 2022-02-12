#!/usr/bin/python3

from StaticTypeCircularBuffer import StaticTypeCircularBuffer

from ServerConfig import ServerConfig

from RtspServerThread import RtspServerThread
from DetectionThread import DetectionThread
from DetectionSenderThread import DetectionSenderThread

from Frame import Frame

from DetectionResult import DetectionResult
from DetectionRenderer import DetectionRenderer

import signal
import sys

def HandleSignal(signal, frame):
    sys.exit(0)

if __name__ == "__main__":
    frameBuffer = StaticTypeCircularBuffer(Frame, 64)
    detectionResultBuffer = StaticTypeCircularBuffer(DetectionResult, 64)

    serverConfig = ServerConfig()
    serverConfig.loadFromConfigFile("ServerConfig.ini")

    rtspServerThread = RtspServerThread(frameBuffer, serverConfig)

    labelFileName = "Darknet/cfg/coco.names"
    configFileName = "Darknet/cfg/yolov4-tiny.cfg"
    weightsFileName = "Darknet/weights/yolov4-tiny.weights"

    confidenceThreshold = 0.3

    detectionThread = DetectionThread(
        labelFileName,
        configFileName,
        weightsFileName,
        confidenceThreshold,
        frameBuffer,
        detectionResultBuffer)

    detectionSenderThread = DetectionSenderThread(
        serverConfig,
        detectionResultBuffer)

    rtspServerThread.start()
    detectionThread.start()
    detectionSenderThread.start()

    #renderer = DetectionRenderer(frameBuffer, detectionResultBuffer)

    #while True:
    #    renderer.render()

    signal.signal(signal.SIGINT, HandleSignal)
    signal.pause()
