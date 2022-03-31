import sys
import numpy as np

from Core.Buffer import Buffer

import gi

gi.require_version('Gst', '1.0')
from gi.repository import Gst, GObject

class VideoStreamer:
    def __init__(self, context):
        self.__context = context

        self.__width = context.width
        self.__height = context.height
        self.__fps = context.fps

        self.__location = context.rtspLocation

        self.__duration = 1 / self.__fps * Gst.SECOND

        self.__framebuffer = context.frameBuffer
        self.__frameCount = 0

        GObject.threads_init()
        Gst.init(None)

    @property
    def width(self):
        return self.__width

    @property
    def height(self):
        return self.__height

    @property
    def fps(self):
        return self.__fps

    @property
    def location(self):
        return self.__location

    def build_pipeline(self):
        self.__pipeline = Gst.parse_launch(
            "appsrc name=m_src caps=video/x-raw,width={},height={},framerate={}/1,format=BGR ! videoconvert !" \
            "x264enc name=m_encoder ! video/x-h264,width=640,height=480,framerate={}/1,format=I420,stream-format=byte-stream !" \
            "rtspclientsink name=m_sink" \
            .format(self.__width, self.__height, self.__fps, self.__fps))
        self.__bus = self.__pipeline.get_bus()

        source = self.__pipeline.get_by_name('m_src')
        source.set_property('is-live', True)
        source.set_property('block', True)
        source.set_property('format', Gst.Format.TIME)
        source.connect('need-data', self.on_need_data)

        encoder = self.__pipeline.get_by_name('m_encoder')
        encoder.set_property('tune', 'zerolatency')

        sink = self.__pipeline.get_by_name('m_sink')
        sink.set_property('location', self.__location)

        #sink.set_property('debug', 1)

    def close_pipeline(self):
        pass

    def get_message(self):
        message = self.__bus.timed_pop(Gst.SECOND)


        if message is not None and message.type in [Gst.MessageType.EOS, Gst.MessageType.ERROR]:
            print("[VideoStreamer]: Can't stream video to server.", file=sys.stderr)

            self.__pipeline.set_state(Gst.State.NULL)
            self.__pipeline.set_state(Gst.State.PLAYING)

        tcpStatus = self.__context.tcpStatus
        rtspStatus = self.__context.rtspStatus

        if tcpStatus != "Connected":
            rtspStatus = "Unconnected"
            self.__pipeline.set_state(Gst.State.NULL)

            print("[VideoStreamer]: Can't stream video to server.", file=sys.stderr)

        if rtspStatus == "Unconnected" and tcpStatus == "Connected":
            self.__pipeline.set_state(Gst.State.PLAYING)
            self.__rtspStatus = "Connected"

            print("[VideoStreamer]: re-start streaming.")

        return True

    def ready(self):
        ret = self.__pipeline.set_state(Gst.State.PLAYING)

        if ret == Gst.StateChangeReturn.FAILURE:
            print("[VideoStreamer]: Failed to set pipeline state.", file=sys.stderr)

        GObject.timeout_add_seconds(3, self.get_message)

    def on_need_data(self, src, length):
        if self.__framebuffer.size <= 0:
            data = np.ndarray(shape=(self.__height, self.__width))
        else:
            frame = self.__framebuffer.tail()
            data = frame.data

        data = data.tostring()

        outerTimestamp = self.__frameCount * self.__duration

        buffer = Gst.Buffer.new_allocate(None, len(data), None)
        buffer.fill(0, data)
        buffer.duration = self.__duration
        buffer.pts = int(outerTimestamp)

        if self.__frameCount % 60 == 0:
            print("[VideoStreamer]: Attempt to send data.(timestamp: {})".format(outerTimestamp))

        retval = src.emit('push-buffer', buffer)

        if retval != Gst.FlowReturn.OK:
            print(retval)

        self.__frameCount += 1
