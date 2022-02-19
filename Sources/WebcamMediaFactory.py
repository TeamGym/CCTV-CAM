import sys
import gi

gi.require_version('Gst', '1.0')
gi.require_version('GstRtspServer', '1.0')
from gi.repository import Gst, GstRtspServer, GObject

from Core.Buffer import Buffer
from Frame import Frame

import cv2

class WebcamMediaFactory(GstRtspServer.RTSPMediaFactory):
    def __init__(self,
                 frameBuffer : Buffer):
        GstRtspServer.RTSPMediaFactory.__init__(self)

    def on_need_data(self, src, length):
        if self.frameBuffer.size <= 0:
            return

        frame = self.frameBuffer.tail()

        data = frame.data
        data = frame.tostring()
        
        timestamp = frame.timestamp

        buffer = Gst.Buffer.new_allocate(None, len(data), None)
        buffer.fill(0, data)
        buffer.duration = self.duration
        buffer.pts = buffer.dts = int(timestamp)

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
        appsrc = rtspMedia.get_element().get_child_by_name('source')
        appsrc.connect('need-data', self.on_need_data)
