#!/usr/bin/python3

from Core.StaticTypeCircularBuffer import StaticTypeCircularBuffer
from Core.Frame import Frame

from Config.ServerConfigLoader import ServerConfigLoader
from Config.StreamingServerConfig import StreamingServerConfig
from Config.DetectionServerConfig import DetectionServerConfig
from Config.HTTPServerConfig import HTTPServerConfig
from Config.CameraConfig import CameraConfig

from Capture.VideoCaptureThread import VideoCaptureThread
from Network.VideoStreamerThread import VideoStreamerThread
from Network.DetectionSenderThread import DetectionSenderThread
from Detect.DetectionThread import DetectionThread

from Detect.DetectionResult import DetectionResult
from Render.DebugRenderer import DebugRenderer

import signal
import sys
import time

def HandleSignal(signal, frame):
    print("Signal detected.")
    sys.exit(0)


frameBuffer = StaticTypeCircularBuffer(Frame, 64)
detectionResultBuffer = StaticTypeCircularBuffer(DetectionResult, 64)

cameraConfig = CameraConfig()
cameraConfig.load("Config/pengca1080p.ini")

videoCaptureThread = VideoCaptureThread(cameraConfig, frameBuffer)

serverConfigLoader = ServerConfigLoader()
serverConfigLoader.load("Config/ServerConfig.ini")

streamingServerConfig = serverConfigLoader.streaming
detectionServerConfig = serverConfigLoader.detection
httpServerConfig = serverConfigLoader.http

videoStreamerThread = VideoStreamerThread(cameraConfig, streamingServerConfig, frameBuffer)

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
    httpServerConfig,
    cameraConfig,
    detectionResultBuffer)

videoCaptureThread.start()
videoStreamerThread.start()
detectionThread.start()
detectionSenderThread.start()

signal.signal(signal.SIGINT, HandleSignal)

renderer = DebugRenderer(frameBuffer, detectionResultBuffer)
renderer.mode = "matplotlib"

while True:
    renderer.render()
    time.sleep(0.01)

