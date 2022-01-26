import sys
import gi

gi.require_version('Gst', '1.0')
gi.require_version('GstRtspServer', '1.0')
from gi.repository import Gst, GstRtspServer, GObject

if __name__ == "__main__":
    gLoop = GObject.MainLoop()
    GObject.threads_init()
    Gst.init(None)

    class WebcamMediaFactory(GstRtspServer.RTSPMediaFactory):
        def __init__(self):
            GstRtspServer.RTSPMediaFactory.__init__(self)

        def do_create_element(self, url):
            src = " v4l2src device=/dev/video0 ! video/x-raw,format=YUY2,framerate=30/1 "
            preEncoding = " videoconvert ! queue"
            encoding = " x264enc "
            payload = " rtph264pay name=pay0 pt=96 "
            return Gst.parse_launch("!".join([src, preEncoding, encoding, payload]))

    class Server:
        def __init__(self):
            self.server = GstRtspServer.RTSPServer()
            self.server.set_service("3002")

            mediaFactory = WebcamMediaFactory()
            mediaFactory.set_shared(True)

            mountPoints = self.server.get_mount_points()
            mountPoints.add_factory("/webcam", mediaFactory)
            
            self.server.attach(None)

    server = Server()

    gLoop.run()
                              
