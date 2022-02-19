import sys
import gi

gi.require_version('Gst', '1.0')
gi.require_version('GstRtspServer', '1.0')
from gi.repository import Gst, GstRtspServer, GObject

from StreamingServerConfig import StreamingServerConfig
from CameraConfig import CameraConfig
from Core.Buffer import Buffer

from WebcamMediaFactory import WebcamMediaFactory

class WebcamServer:
    def __init__(self,
                 service : str,
                 mountpoint: str,
                 frameBuffer : Buffer):
        self.server = GstRtspServer.RTSPServer()
        self.server.set_service(service)

        mediaFactory = WebcamMediaFactory(frameBuffer)
        mediaFactory.set_shared(True)

        mountPoints = self.server.get_mount_points()
        mountPoints.add_factory(mountpoint, mediaFactory)

        self.server.attach(None)
