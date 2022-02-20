import sys

from threading import Thread

from Core.Buffer import Buffer

from StreamingServerConfig import StreamingServerConfig
from threading import Thread

from CameraConfig import CameraConfig

from VideoStreamer import VideoStreamer

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

        host = serverConfig.host
        port = serverConfig.port

        self.videoStreamer = VideoStreamer(width, height, fps, host, port, framebuffer)

    def run(self):
        self.videoStreamer.ready()
        
        gLoop = GObject.MainLoop()
        gLoop.run()
