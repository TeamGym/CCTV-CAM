#!/usr/bin/python3

from Core.StaticTypeCircularBuffer import StaticTypeCircularBuffer

from ServerConfigLoader import ServerConfigLoader
from StreamingServerConfig import StreamingServerConfig
from DetectionServerConfig import DetectionServerConfig
from CameraConfig import CameraConfig

from VideoCaptureThread import VideoCaptureThread
from StreamingServerThread import StreamingServerThread
from DetectionThread import DetectionThread
from DetectionSenderThread import DetectionSenderThread

from Frame import Frame

from DetectionResult import DetectionResult
from DebugRenderer import DebugRenderer

import signal
import sys

def HandleSignal(signal, frame):
    print("Signal detected.")
    sys.exit(0)

if __name__ == "__main__":
    frameBuffer = StaticTypeCircularBuffer(Frame, 64)
    detectionResultBuffer = StaticTypeCircularBuffer(DetectionResult, 64)
    
    cameraConfig = CameraConfig()
    cameraConfig.load("pengca1080p.ini")

    videoCaptureThread = VideoCaptureThread(cameraConfig, frameBuffer)

    serverConfigLoader = ServerConfigLoader()
    serverConfigLoader.load("ServerConfig.ini")

    streamingServerConfig = serverConfigLoader.streaming
    detectionServerConfig = serverConfigLoader.detection

    streamingServerThread = StreamingServerThread(cameraConfig, streamingServerConfig, frameBuffer)

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
        detectionServerConfig,
        detectionResultBuffer)

    videoCaptureThread.start()
    streamingServerThread.start()
    detectionThread.start()
    detectionSenderThread.start()

    signal.signal(signal.SIGINT, HandleSignal)

    renderer = DebugRenderer(frameBuffer, detectionResultBuffer)
    renderer.mode = "matplotlib"

    while True:
        renderer.render()
