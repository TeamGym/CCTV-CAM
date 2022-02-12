import sys
import gi

from threading import Thread

from Buffer import Buffer
from ServerConfig import ServerConfig
from WebcamMediaFactory import WebcamMediaFactory
from WebcamServer import WebcamServer

import gi

gi.require_version('Gst', '1.0')
gi.require_version('GstRtspServer', '1.0')
from gi.repository import Gst, GstRtspServer, GObject

class RtspServerThread(Thread):
    def __init__(self,
                 frameBuffer : Buffer,
                 serverConfig : ServerConfig):
        super().__init__()

        GObject.threads_init()
        Gst.init(None)

        server = WebcamServer(serverConfig, frameBuffer)
        
    def run(self):
        gLoop = GObject.MainLoop()
        gLoop.run()
