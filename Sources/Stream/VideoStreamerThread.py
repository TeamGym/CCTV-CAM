import sys

from threading import Thread

from Core.Buffer import Buffer

from Config.StreamingServerConfig import StreamingServerConfig
from Config.CameraConfig import CameraConfig

from Stream.VideoStreamer import VideoStreamer

import gi

gi.require_version('Gst', '1.0')
from gi.repository import Gst, GObject

class VideoStreamerThread(Thread):
    def __init__(self,
                 cameraConfig : CameraConfig,
                 serverConfig : StreamingServerConfig,
                 framebuffer : Buffer):
        super().__init__()

        width = cameraConfig.width
        height = cameraConfig.height
        fps = cameraConfig.fps

        location = serverConfig.location

        self.videoStreamer = VideoStreamer(width, height, fps, location, framebuffer)

    def run(self):
        self.videoStreamer.ready()
        
        gLoop = GObject.MainLoop()
        gLoop.run()
