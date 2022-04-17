#!/usr/bin/python3

from Core.Buffer import Buffer
from Core.BufferHolder import BufferHolder
from Core.BufferBroadcaster import BufferBroadcaster

from Config.JSONConfig import JSONConfig

from Capture.VideoCapture import VideoCapture
from Detect.MotionDetector import MotionDetector
from Detect.ObjectDetector import ObjectDetector
from Network.VideoStreamer import VideoStreamer
from Network.RemoteServerConnector import RemoteServerConnector
from Network.ConnectionHolder import ConnectionHolder

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

config = JSONConfig()
config.loadFile("Setting/AMD64/default-test.json")

bufferHolder = BufferHolder()
bufferHolder.connectBuffers(
    sockets={
        "Video": BufferBroadcaster(
            sockets={
                "Stream": Buffer(maxlen=500),
                "Object": Buffer(maxlen=500),
                "Motion": Buffer(maxlen=500),
                "Render": Buffer(maxlen=100)
            }),
        "ObjectOut": Buffer(maxlen=500),
        "ObjectRender": Buffer(maxlen=100),
        "MotionOut": Buffer(maxlen=500),
        "MotionRender": Buffer(maxlen=100),
        "Command": Buffer()
    })

connectionHolder = ConnectionHolder()
connectionHolder.addConnections(["TCP", "VideoStream"])

videoCapture = VideoCapture(bufferHolder.getBuffer("Video"))
videoCapture.openDevice(
    config.device.camera.device,
    config.device.camera.width,
    config.device.camera.height,
    config.device.camera.fps)

videoStreamer =  VideoStreamer(
    config=config,
    connectionHolder=connectionHolder,
    videoBuffer=bufferHolder.getBuffer("Video").getBuffer("Stream"))
remoteServerConnector = RemoteServerConnector(
    config=config,
    connectionHolder=connectionHolder,
    objectBuffer=bufferHolder.getBuffer("ObjectOut"),
    motionBuffer=bufferHolder.getBuffer("MotionOut"),
    commandQueue=bufferHolder.getBuffer("Command"))

motionDetector = MotionDetector(
    config=config,
    videoBuffer=bufferHolder.getBuffer("Video").getBuffer("Motion"),
    outputBuffer=bufferHolder.getBuffer("MotionOut"),
    renderBuffer=bufferHolder.getBuffer("MotionRender"))
objectDetector = ObjectDetector(
    config=config,
    videoBuffer=bufferHolder.getBuffer("Video").getBuffer("Object"),
    outputBuffer=bufferHolder.getBuffer("ObjectOut"),
    renderBuffer=bufferHolder.getBuffer("ObjectRender"))

videoCaptureThread = ThreadLoopRunner(videoCapture.read)
videoStreamerThread = ThreadRunner(videoStreamer.start)
motionDetectorThread = ThreadLoopRunner(motionDetector.detect)
objectDetectorThread = ThreadLoopRunner(objectDetector.detect)
connectorThread = ThreadRunner(remoteServerConnector.communicate_automatically)

monitors = [
    RenderableMonitor(name="Original",
                      buffer=bufferHolder.getBuffer("Video").getBuffer("Render"),
                      left=0,
                      top=0,
                      width=config.device.camera.width,
                      height=config.device.camera.height),
    RenderableMonitor(name="Motion",
                      buffer=bufferHolder.getBuffer("MotionRender"),
                      left=600,
                      top=0,
                      width=config.device.camera.width,
                      height=config.device.camera.height),
    RenderableMonitor(name="Object",
                      buffer=bufferHolder.getBuffer("ObjectRender"),
                      left=1200,
                      top=0,
                      width=config.device.camera.width,
                      height=config.device.camera.height)
]

renderer = BufferViewer(30, monitors=monitors)

videoCaptureThread.start()
videoStreamerThread.start()
motionDetectorThread.start()
objectDetectorThread.start()
connectorThread.start()

pyglet.app.run()

signal.signal(signal.SIGINT, HandleSignal)
