import sys
import gi

from threading import Thread

from Core.Buffer import Buffer

from StreamingServerConfig import StreamingServerConfig
from CameraConfig import CameraConfig 
from WebcamMediaFactory import WebcamMediaFactory
from WebcamServer import WebcamServer

import gi

gi.require_version('Gst', '1.0')
gi.require_version('GstRtspServer', '1.0')
from gi.repository import Gst, GstRtspServer, GObject

class StreamingServerThread(Thread):
    def __init__(self,
                 cameraConfig : CameraConfig,
                 serverConfig : StreamingServerConfig,
                 frameBuffer : Buffer):
        super().__init__()

        GObject.threads_init()
        Gst.init(None)

        service = serverConfig.service
        mountpoint = serverConfig.mountpoint

        self.server = WebcamServer(service, mountpoint, cameraConfig, frameBuffer)
        
    def run(self):
        gLoop = GObject.MainLoop()
        gLoop.run()
