#!/usr/bin/python3

from Config.JSONConfig import JSONConfig
from MainContext import MainContext

from Capture.VideoCapture import VideoCapture
from Detect.MotionDetector import MotionDetector
from Detect.ObjectDetector import ObjectDetector
from Network.VideoStreamer import VideoStreamer
from Network.RemoteServerConnector import RemoteServerConnector

from Thread.ThreadRunner import ThreadRunner
from Thread.ThreadLoopRunner import ThreadLoopRunner

from Render.RenderableMonitor import RenderableMonitor
from Render.BufferViewer import BufferViewer

import signal
import sys
import pyglet

def HandleSignal(signal, frame):
    print("Signal detected.")
    sys.exit(0)

cameraConfig = JSONConfig("Setting/laptopWebcam.json")
detectorConfig = JSONConfig("Setting/yolo-gun.json")
serverConfig = JSONConfig("Setting/remote-test-server.json")

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
videoStreamer =  VideoStreamer(context)
remoteServerConnector = RemoteServerConnector(context)
motionDetector = MotionDetector(context)
objectDetector = ObjectDetector(
    detectorConfig.label,
    detectorConfig.config,
    detectorConfig.weights,
    detectorConfig.confidenceThreshold,
    context)

videoCaptureThread = ThreadLoopRunner(videoCapture.read)
videoStreamerThread = ThreadRunner(videoStreamer.start)
motionDetectorThread = ThreadLoopRunner(motionDetector.detect)
objectDetectorThread = ThreadLoopRunner(objectDetector.detect)
connectorThread = ThreadRunner(remoteServerConnector.communicate_automatically)

monitors = [
    RenderableMonitor(name="Capture",
                      buffer=videoCapture.monitorBuffer,
                      left=0,
                      top=0,
                      width=context.width,
                      height=context.height),
    RenderableMonitor(name="Capture",
                      buffer=motionDetector.monitorBuffer,
                      left=600,
                      top=0,
                      width=context.width,
                      height=context.height),
    RenderableMonitor(name="Capture",
                      buffer=objectDetector.monitorBuffer,
                      left=1200,
                      top=0,
                      width=context.width,
                      height=context.height)
]

renderer = BufferViewer(30, monitors=monitors)

videoCaptureThread.start()
videoStreamerThread.start()
motionDetectorThread.start()
objectDetectorThread.start()
connectorThread.start()

pyglet.app.run()

signal.signal(signal.SIGINT, HandleSignal)
