import sys
import gi

gi.require_version('Gst', '1.0')
gi.require_version('GstRtspServer', '1.0')
from gi.repository import Gst, GstRtspServer, GObject

from CameraConfig import CameraConfig

from Buffer import Buffer
from Frame import Frame


import cv2

class WebcamMediaFactory(GstRtspServer.RTSPMediaFactory):
    def __init__(self,
                 cameraConfig : CameraConfig, 
                 frameBuffer : Buffer):
        GstRtspServer.RTSPMediaFactory.__init__(self)

        self.device = cameraConfig.device
        self.width = cameraConfig.width
        self.height = cameraConfig.height
        self.fps = cameraConfig.fps
        self.format = cameraConfig.format
        
        self.capture = cv2.VideoCapture(self.device)
        self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
        self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)
        self.capture.set(cv2.CAP_PROP_FPS, self.fps)
        
        self.duration = 1 / self.fps * Gst.SECOND
        self.frameCount = 0

        if not self.capture.isOpened():
            print("[cv2.VideoCapture]: can't open")
            sys.exit()

        self.frameBuffer = frameBuffer

    def on_need_data(self, src, length):
        if not self.capture.isOpened():
            return

        ret, frame = self.capture.read()

        if not ret:
            return

        data = frame.tostring()
        timestamp = self.frameCount * self.duration

        buffer = Gst.Buffer.new_allocate(None, len(data), None)
        buffer.fill(0, data)
        buffer.duration = self.duration
        buffer.pts = buffer.dts = int(timestamp)

        self.frameCount += 1

        frame = Frame(timestamp, frame)
        self.frameBuffer.add(frame)

        retval = src.emit('push-buffer', buffer)

        if retval != Gst.FlowReturn.OK:
            print(retval)

    def do_create_element(self, url):
        launchString = "appsrc name=source is-live=true block=true format=GST_FORMAT_TIME" \
                       " caps=video/x-raw,width={},height={},framerate={}/1,format=BGR ! videoconvert" \
                       " ! queue ! omxh264enc ! rtph264pay config-interval=1 name=pay0 pt=96".format(
                           self.width,
                           self.height,
                           self.fps)
        return Gst.parse_launch(launchString)

    def do_configure(self, rtspMedia):
        self.frameCount = 0

        appsrc = rtspMedia.get_element().get_child_by_name('source')
        appsrc.connect('need-data', self.on_need_data)
