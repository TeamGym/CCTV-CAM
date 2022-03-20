import sys
import numpy as np

from Core.Buffer import Buffer

import gi

gi.require_version('Gst', '1.0')
from gi.repository import Gst, GObject

class VideoStreamer:
    def __init__(self, context):
        self.context = context

        self.width = context.width
        self.height = context.height
        self.fps = context.fps

        self.location = context.rtspLocation

        self.duration = 1 / self.fps * Gst.SECOND

        self.framebuffer = context.frameBuffer
        self.frameCount = 0

        GObject.threads_init()
        Gst.init(None)

    def build_pipeline(self):
        self.pipeline = Gst.parse_launch(
            "appsrc name=m_src caps=video/x-raw,width={},height={},framerate={}/1,format=BGR ! videoconvert !" \
            "x264enc name=m_encoder ! video/x-h264,width=640,height=480,framerate={}/1,format=I420,stream-format=byte-stream !" \
            "rtspclientsink name=m_sink" \
            .format(self.width, self.height, self.fps, self.fps))
        self.bus = self.pipeline.get_bus()

        source = self.pipeline.get_by_name('m_src')
        source.set_property('is-live', True)
        source.set_property('block', True)
        source.set_property('format', Gst.Format.TIME)
        source.connect('need-data', self.on_need_data)

        encoder = self.pipeline.get_by_name('m_encoder')
        encoder.set_property('tune', 'zerolatency')

        sink = self.pipeline.get_by_name('m_sink')
        sink.set_property('location', self.location)

        #sink.set_property('debug', 1)

    def close_pipeline(self):
        pass

    def get_message(self):
        message = self.bus.timed_pop(Gst.SECOND)


        if message is not None and message.type in [Gst.MessageType.EOS, Gst.MessageType.ERROR]:
            print("[VideoStreamer]: Can't stream video to server.", file=sys.stderr)

            self.pipeline.set_state(Gst.State.NULL)
            self.pipeline.set_state(Gst.State.PLAYING)

        tcpStatus = self.context.tcpStatus
        rtspStatus = self.context.rtspStatus

        if tcpStatus != "Connected":
            rtspStatus = "Unconnected"
            self.pipeline.set_state(Gst.State.NULL)

            print("[VideoStreamer]: Can't stream video to server.", file=sys.stderr)

        if rtspStatus == "Unconnected" and tcpStatus == "Connected":
            self.pipeline.set_state(Gst.State.PLAYING)
            self.rtspStatus = "Connected"

            print("[VideoStreamer]: re-start streaming.")

        return True

    def ready(self):
        ret = self.pipeline.set_state(Gst.State.PLAYING)

        if ret == Gst.StateChangeReturn.FAILURE:
            print("[VideoStreamer]: Failed to set pipeline state.", file=sys.stderr)

        GObject.timeout_add_seconds(3, self.get_message)

    def on_need_data(self, src, length):
        if self.framebuffer.size <= 0:
            data = np.ndarray(shape=(self.height, self.width))
        else:
            frame = self.framebuffer.tail()
            data = frame.data

        data = data.tostring()

        outerTimestamp = self.frameCount * self.duration

        buffer = Gst.Buffer.new_allocate(None, len(data), None)
        buffer.fill(0, data)
        buffer.duration = self.duration
        buffer.pts = int(outerTimestamp)

        if self.frameCount % 60 == 0:
            print("[VideoStreamer]: Attempt to send data.(timestamp: {})".format(outerTimestamp))

        retval = src.emit('push-buffer', buffer)

        if retval != Gst.FlowReturn.OK:
            print(retval)

        self.frameCount += 1
