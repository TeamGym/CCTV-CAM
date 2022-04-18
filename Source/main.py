#!/usr/bin/python3

from Core.Buffer import Buffer
from Core.BufferHolder import BufferHolder
from Core.BufferBroadcaster import BufferBroadcaster
from Core.JSON import JSON

from Capture.VideoCapture import VideoCapture

from Audio.AudioDeviceController import AudioDeviceController
from Audio.TTSEngine import TTSEngine
from Audio.MotionAlerter import MotionAlerter
from Audio.ObjectAlerter import ObjectAlerter

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

config = JSON()
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
        "ObjectOut": BufferBroadcaster(
            sockets={
                "Send": Buffer(),
                "Alert": Buffer()
            }
        ),
        "ObjectRender": Buffer(maxlen=100),
        "MotionOut": BufferBroadcaster(
            sockets={
                "Send": Buffer(),
                "Alert": Buffer()
            }
        ),
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

ttsEngine = TTSEngine()
ttsEngine.start()

renderer = BufferViewer(30, monitors=monitors)

threads = [
    ThreadLoopRunner(
        func=videoCapture.read),
    ThreadLoopRunner(
        func=motionDetector.detect,
        minInterval=1/config.detector.motion.targetFPS),
    ThreadLoopRunner(
        func=objectDetector.detect,
        minInterval=1/config.detector.object.targetFPS),
    VideoStreamer(
        config=config,
        connectionHolder=connectionHolder,
        videoBuffer=bufferHolder.getBuffer("Video").getBuffer("Stream")),
    RemoteServerConnector(
        config=config,
        connectionHolder=connectionHolder,
        objectBuffer=bufferHolder.getBuffer("ObjectOut").getBuffer("Send"),
        motionBuffer=bufferHolder.getBuffer("MotionOut").getBuffer("Send"),
        commandQueue=bufferHolder.getBuffer("Command")),
    MotionAlerter(
        config=config,
        detectionBuffer=bufferHolder.getBuffer("MotionOut").getBuffer("Alert"),
        engine=ttsEngine),
    ObjectAlerter(
        config=config,
        detectionBuffer=bufferHolder.getBuffer("ObjectOut").getBuffer("Alert"),
        engine=ttsEngine)
]

for thread in threads:
    thread.start()

pyglet.app.run()
signal.signal(signal.SIGINT, HandleSignal)
