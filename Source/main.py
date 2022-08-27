#!/usr/bin/python3

from Core import Buffer, BufferHolder, BufferBroadcaster, JSON
from Thread import ThreadRunner, ThreadLoopRunner
from Video import VideoCapture, ClipExporter
from Audio import AudioDeviceController, TTSEngine, MotionAlerter, ObjectAlerter
from Detect import MotionDetector, ObjectDetector
from Network import ConnectionHolder, VideoStreamer, RemoteServerConnector
from Log import MotionLogger, ObjectLogger
from Render import RenderableMonitor, BufferViewer

import signal
import os
import sys
import time
import pyglet
import pyglet.window.key as pyglet_key
import tkinter
from tkinter import filedialog

def HandleSignal(signal, frame):
    print("Signal detected.")
    sys.exit(0)

root = tkinter.Tk()
root.withdraw()

configFileName = filedialog.askopenfilename(title='Choose config file')

config = JSON()
config.loadFile(configFileName)

bufferHolder = BufferHolder()
bufferHolder.connectBuffers(
    sockets={
        "Video": BufferBroadcaster(
            sockets={
                "Stream": Buffer(maxlen=500),
                "Object": Buffer(maxlen=500),
                "Motion": Buffer(maxlen=500),
                "Render": Buffer(maxlen=100),
                "Record": Buffer()
            }),
        "ObjectOut": BufferBroadcaster(
            sockets={
                "Send": Buffer(),
                "Alert": Buffer(),
                "Log": Buffer()
            }),
        "ObjectRender": Buffer(maxlen=100),
        "MotionOut": BufferBroadcaster(
            sockets={
                "Send": Buffer(),
                "Alert": Buffer(),
                "Log": Buffer()
            }),
        "MotionRender": Buffer(maxlen=100),
        "Command": Buffer()
    })

connectionHolder = ConnectionHolder()
connectionHolder.addConnections(["TCP", "VideoStream"])

print("Creating Video Capture...")
print("    Device: {}".format(config.device.camera.device))
print("    Size: ({}, {})".format(config.device.camera.width, config.device.camera.height))
print("    Framerate: {}".format(config.device.camera.fps))

videoCapture = VideoCapture(bufferHolder.getBuffer("Video"))
videoCapture.openDevice(
    config.device.camera.device,
    config.device.camera.width,
    config.device.camera.height,
    config.device.camera.fps)

print("Successfully created video capture.")

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

print("Initializing TTS Engine...")

ttsEngine = TTSEngine()
ttsEngine.start()

print("Successfully initialized TTS Engine.")

print("Initializing Renderer...")

renderer = BufferViewer(60, monitors=monitors)

print("Successfully initialized Renderer.")

print("Initializing main system...")

os.makedirs("../Log/" + time.strftime("%Y-%m-%d"), exist_ok=True)

threads = [
    ThreadLoopRunner(
        func=videoCapture.read),
    ObjectDetector(
        config=config.detector.object.config,
        weights=config.detector.object.weights,
        label=config.detector.object.label,
        threshold=config.detector.object.threshold,
        targetFPS=config.detector.object.targetFPS,
        videoBuffer=bufferHolder.getBuffer("Video").getBuffer("Object"),
        outputBuffer=bufferHolder.getBuffer("ObjectOut"),
        renderBuffer=bufferHolder.getBuffer("ObjectRender")),
    MotionDetector(
        updateInterval=config.detector.motion.updateInterval,
        updateThreshold=config.detector.motion.updateThreshold,
        motionThreshold=config.detector.motion.motionThreshold,
        targetFPS=config.detector.motion.targetFPS,
        videoBuffer=bufferHolder.getBuffer("Video").getBuffer("Motion"),
        outputBuffer=bufferHolder.getBuffer("MotionOut"),
        renderBuffer=bufferHolder.getBuffer("MotionRender")),
    RemoteServerConnector(
        host=config.network.tcp.host,
        port=config.network.tcp.port,
        videoWidth=config.device.camera.width,
        videoHeight=config.device.camera.height,
        videoFramerate=config.device.camera.fps,
        cameraId=config.device.camera.id,
        connectionHolder=connectionHolder,
        videoBuffer=bufferHolder.getBuffer("Video").getBuffer("Stream"),
        objectBuffer=bufferHolder.getBuffer("ObjectOut").getBuffer("Send"),
        motionBuffer=bufferHolder.getBuffer("MotionOut").getBuffer("Send"),
        commandQueue=bufferHolder.getBuffer("Command"),ID=1)
]

print("Initializing Components...")
print("    Recorder: {}".format(config.component.record))
print("    Alerter: {}".format(config.component.alert))
print("    Logger: {}".format(config.component.log))

if config.component.record:
    recorder = ClipExporter(
        prefix="../Clip/",
        fourcc=config.video.clip.fourcc,
        extension=config.video.clip.extension,
        width=config.video.clip.width,
        height=config.video.clip.height,
        fps=config.video.clip.fps,
        clipLength=config.video.clip.length,
        videoBuffer=bufferHolder.getBuffer("Video").getBuffer("Record"))

    threads.append(recorder)

if config.component.alert:
    motionAlerter = MotionAlerter(
        interval=config.audio.alert.motion.interval,
        cooldown=config.audio.alert.motion.cooldown,
        detectionBuffer=bufferHolder.getBuffer("MotionOut").getBuffer("Alert"),
        engine=ttsEngine)

    objectAlerter = ObjectAlerter(
        interval=config.audio.alert.object.interval,
        targets=config.audio.alert.object.targets,
        cooldown=config.audio.alert.object.cooldown,
        detectionBuffer=bufferHolder.getBuffer("ObjectOut").getBuffer("Alert"),
        engine=ttsEngine)

    threads.append(motionAlerter)
    threads.append(objectAlerter)

if config.component.log:
    motionLogger = MotionLogger(
        filePath=time.strftime('../Log/%Y-%m-%d/Motion_%H_%M_%S', time.localtime()),
        detectionBuffer=bufferHolder.getBuffer("MotionOut").getBuffer("Log"))

    objectLogger = ObjectLogger(
        filePath=time.strftime('../Log/%Y-%m-%d/Object_%H_%M_%S', time.localtime()),
        detectionBuffer=bufferHolder.getBuffer("ObjectOut").getBuffer("Log"))

    threads.append(motionLogger)
    threads.append(objectLogger)

print("Successfully initialized all components.")

for thread in threads:
    thread.start()

print("Successfully initialized main system.")

def keydownCallback(key):
    global threads
    if key == pyglet_key.Q:
        for thread in threads:
            thread.isRunning = False

renderer.addEventHandler("KeyDown", keydownCallback)

print("Running Application...")

pyglet.app.run()
signal.signal(signal.SIGINT, HandleSignal)
