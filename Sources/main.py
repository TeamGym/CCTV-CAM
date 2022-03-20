#!/usr/bin/python3

from Config.Config import Config
from Config.CameraConfig import CameraConfig
from Config.DetectorConfig import DetectorConfig
from Config.ServerConfigLoader import ServerConfigLoader
from Config.RTSPServerConfig import RTSPServerConfig
from Config.TCPServerConfig import TCPServerConfig

from MainContext import MainContext

from Capture.VideoCapture import VideoCapture
from Detect.Detector import Detector
from Network.VideoStreamer import VideoStreamer
from Network.DetectionSender import DetectionSender

from Thread.VideoCaptureThread import VideoCaptureThread
from Thread.VideoStreamerThread import VideoStreamerThread
from Thread.DetectionSenderThread import DetectionSenderThread
from Thread.DetectionThread import DetectionThread

from Render.Renderer import Renderer

import signal
import sys
import pyglet

def HandleSignal(signal, frame):
    print("Signal detected.")
    sys.exit(0)

cameraConfig = CameraConfig()
cameraConfig.load("laptopWebcam.ini")

detectorConfig = DetectorConfig()
detectorConfig.load("yolo-gun.ini")

serverConfigLoader = ServerConfigLoader()
serverConfigLoader.load("main-server.ini")

rtspServerConfig = serverConfigLoader.rtsp
tcpServerConfig = serverConfigLoader.tcp

context = MainContext(
    cameraConfig.device,
    cameraConfig.width,
    cameraConfig.height,
    cameraConfig.fps,
    cameraConfig.format,
    rtspServerConfig.location,
    tcpServerConfig.host,
    tcpServerConfig.port)

videoCapture = VideoCapture(context)
videoCaptureThread = VideoCaptureThread(videoCapture)

videoStreamer =  VideoStreamer(context)
videoStreamerThread = VideoStreamerThread(videoStreamer)

detector = Detector(
    detectorConfig.label,
    detectorConfig.config,
    detectorConfig.weights,
    detectorConfig.confidenceThreshold,
    context.frameBuffer,
    context.detectionBuffer)
detectionThread = DetectionThread(detector)

detectionSender = DetectionSender(context)
detectionSenderThread = DetectionSenderThread(detectionSender)

renderer = Renderer(context)

videoCaptureThread.start()
videoStreamerThread.start()
detectionThread.start()
detectionSenderThread.start()

pyglet.app.run()

signal.signal(signal.SIGINT, HandleSignal)
