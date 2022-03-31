#!/usr/bin/python3
from Config.JSONConfig import JSONConfig
from MainContext import MainContext

from Capture.VideoCapture import VideoCapture
from Detect.MotionDetector import MotionDetector
from Detect.ObjectDetector import ObjectDetector
from Network.VideoStreamer import VideoStreamer
from Network.RemoteServerConnector import RemoteServerConnector

from Thread.VideoCaptureThread import VideoCaptureThread
from Thread.VideoStreamerThread import VideoStreamerThread
from Thread.DetectorThread import DetectorThread
from Thread.RemoteServerConnectorThread import RemoteServerConnectorThread

from Render.Renderer import Renderer

import signal
import sys
import pyglet

def HandleSignal(signal, frame):
    print("Signal detected.")
    sys.exit(0)

cameraConfig = JSONConfig("laptopWebcam.json")
detectorConfig = JSONConfig("yolo-gun.json")
serverConfig = JSONConfig("remote-test-server.json")

context = MainContext(
    cameraConfig.device,
    cameraConfig.width,
    cameraConfig.height,
    cameraConfig.fps,
    cameraConfig.format,
    serverConfig.rtspLocation,
    serverConfig.tcpHost,
    serverConfig.tcpPort)
videoCapture = VideoCapture(context)
videoCaptureThread = VideoCaptureThread(videoCapture)

videoStreamer =  VideoStreamer(context)
videoStreamerThread = VideoStreamerThread(videoStreamer)

motionDetector = MotionDetector(
    context.frameBuffer,
    context.differenceBuffer)
objectDetector = ObjectDetector(
    detectorConfig.label,
    detectorConfig.config,
    detectorConfig.weights,
    detectorConfig.confidenceThreshold,
    context.frameBuffer,
    context.detectionBuffer)
motionDetectorThread = DetectorThread(motionDetector)
objectDetectorThread = DetectorThread(objectDetector)

remoteServerConnector = RemoteServerConnector(context)
connectorThread = RemoteServerConnectorThread(remoteServerConnector)

renderer = Renderer(context)

videoCaptureThread.start()
videoStreamerThread.start()
motionDetectorThread.start()
objectDetectorThread.start()
connectorThread.start()

pyglet.app.run()

signal.signal(signal.SIGINT, HandleSignal)
