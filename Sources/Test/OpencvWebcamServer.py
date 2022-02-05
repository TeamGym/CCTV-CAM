import sys
import cv2

import gi

gi.require_version('Gst', '1.0')
gi.require_version('GstRtspServer', '1.0')
from gi.repository import Gst, GstRtspServer, GObject

if __name__ == "__main__":
    class WebcamMediaFactory(GstRtspServer.RTSPMediaFactory):
        def __init__(self):
            GstRtspServer.RTSPMediaFactory.__init__(self)

            self.width = 1280
            self.height = 720
            self.fps = 10

            self.capture = cv2.VideoCapture(0)
            self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
            self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)
            self.capture.set(cv2.CAP_PROP_FPS, self.fps)
            self.duration = 1 / self.fps * Gst.SECOND
            self.frameCount = 0

            if not self.capture.isOpened():
                print("[cv2.VideoCapture]: can't open")
                sys.exit()

        def on_need_data(self, src, length):
            if not self.capture.isOpened():
                return
            
            ret, frame = self.capture.read()

            print(frame.shape)
                
            if not ret:
                return

            data = frame.tostring()
            timestamp = self.frameCount * self.duration
            
            buffer = Gst.Buffer.new_allocate(None, len(data), None)
            buffer.fill(0, data)
            buffer.duration = self.duration
            buffer.pts = buffer.dts = int(timestamp)
            
            self.frameCount += 1            
            retval = src.emit('push-buffer', buffer)

            if retval != Gst.FlowReturn.OK:
                print(retval)

        def do_create_element(self, url):            
            launchString = "appsrc name=source is-live=true block=true format=GST_FORMAT_TIME" \
                           " caps=video/x-raw,width=1280,height=720,framerate=10/1,format=BGR ! videoconvert" \
                           " ! omxh264enc ! rtph264pay config-interval=1 name=pay0 pt=96"
            print(launchString)
            return Gst.parse_launch(launchString)

        def do_configure(self, rtspMedia):
            self.frameCount = 0
            
            appsrc = rtspMedia.get_element().get_child_by_name('source')
            appsrc.connect('need-data', self.on_need_data)

    class WebcamServer:
        def __init__(self):
            self.server = GstRtspServer.RTSPServer()
            self.server.set_service("3002")

            mediaFactory = WebcamMediaFactory()
            mediaFactory.set_shared(True)

            mountPoints = self.server.get_mount_points()
            mountPoints.add_factory("/webcam", mediaFactory)
            
            self.server.attach(None)

    GObject.threads_init()
    Gst.init(None)

    server = WebcamServer()
    
    gLoop = GObject.MainLoop()
    gLoop.run()
                              
