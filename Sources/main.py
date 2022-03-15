#!/usr/bin/python3

from Core.StaticTypeCircularBuffer import StaticTypeCircularBuffer
from Core.Frame import Frame

from Config.CameraConfig import CameraConfig
from Config.DetectorConfig import DetectorConfig
from Config.ServerConfigLoader import ServerConfigLoader
from Config.StreamingServerConfig import StreamingServerConfig
from Config.DetectionServerConfig import DetectionServerConfig
from Config.HTTPServerConfig import HTTPServerConfig

from Capture.VideoCapture import VideoCapture
from Detect.Detector import Detector
from Network.VideoStreamer import VideoStreamer
from Network.DetectionSender import DetectionSender

from VideoCaptureThread import VideoCaptureThread
from VideoStreamerThread import VideoStreamerThread
from DetectionSenderThread import DetectionSenderThread
from DetectionThread import DetectionThread

from Detect.Detection import Detection

from Render.Renderer import Renderer

import signal
import sys
import time
import pyglet

def HandleSignal(signal, frame):
    print("Signal detected.")
    sys.exit(0)

frameBuffer = StaticTypeCircularBuffer(Frame, 64)
detectionBuffer = StaticTypeCircularBuffer(Detection, 64)

cameraConfig = CameraConfig()
cameraConfig.load("laptopWebcam.ini")

detectorConfig = DetectorConfig()
detectorConfig.load("yolo-gun.ini")

serverConfigLoader = ServerConfigLoader()
serverConfigLoader.load("main-server.ini")

streamingServerConfig = serverConfigLoader.streaming
detectionServerConfig = serverConfigLoader.detection
httpServerConfig = serverConfigLoader.http

videoCapture = VideoCapture(
    cameraConfig.device,
    cameraConfig.width,
    cameraConfig.height,
    cameraConfig.fps,
    cameraConfig.format,
    frameBuffer)
videoCaptureThread = VideoCaptureThread(videoCapture)

videoStreamer =  VideoStreamer(
    cameraConfig.width,
    cameraConfig.height,
    cameraConfig.fps,
    streamingServerConfig.location,
    frameBuffer)
videoStreamerThread = VideoStreamerThread(videoStreamer)

detector = Detector(
    detectorConfig.label,
    detectorConfig.config,
    detectorConfig.weights,
    detectorConfig.confidenceThreshold,
    frameBuffer,
    detectionBuffer)
detectionThread = DetectionThread(detector)

detectionSender = DetectionSender(
    detectionServerConfig.host,
    detectionServerConfig.port,
    httpServerConfig.url,
    cameraConfig.width,
    cameraConfig.height,
    detectionBuffer)
detectionSenderThread = DetectionSenderThread(detectionSender)

renderer = Renderer(
    cameraConfig.width,
    cameraConfig.height,
    cameraConfig.fps,
    frameBuffer,
    detectionBuffer)

videoCaptureThread.start()
videoStreamerThread.start()
detectionThread.start()
detectionSenderThread.start()

pyglet.app.run()

signal.signal(signal.SIGINT, HandleSignal)
