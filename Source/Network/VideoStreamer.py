import time
import sys
import numpy as np

import gi

gi.require_version('Gst', '1.0')
from gi.repository import Gst, GObject

from Thread import ThreadRunner

class VideoStreamer(ThreadRunner):
    def __init__(self, width, height, fps, host, port, videoBuffer):
        super().__init__(func=self.startPipeline)

        self.__width = width
        self.__height = height
        self.__fps = fps

        self.__host = host
        self.__port = port

        self.__duration = 1 / self.__fps * Gst.SECOND

        self.__videoBuffer = videoBuffer
        self.__frameCount = 0

        GObject.threads_init()
        Gst.init(None)

    def build_pipeline(self):
        self.__pipeline = Gst.parse_launch(
            "appsrc name=m_src caps=video/x-raw,width={},height={},framerate={}/1,format=BGR ! "
            "videoconvert ! "
            "x264enc name=m_encoder ! " # edit
            "video/x-h264,width={},height={},framerate={}/1,format=I420,stream-format=byte-stream,profile=constrained-baseline ! "
            "udpsink name=m_sink"
            .format(self.__width, self.__height, self.__fps, self.__width, self.__height, self.__fps))
        self.__bus = self.__pipeline.get_bus()

        source = self.__pipeline.get_by_name('m_src')
        source.set_property('is-live', True)
        source.set_property('block', True)
        source.set_property('format', Gst.Format.TIME)
        source.set_property('do-timestamp', True)
        source.connect('need-data', self.on_need_data)

        encoder = self.__pipeline.get_by_name('m_encoder')
        encoder.set_property('tune', 'zerolatency')
        encoder.set_property('speed-preset', 'ultrafast')
        encoder.set_property('key-int-max', 60)
        encoder.set_property('bitrate', 3000)
        #encoder.set_property('rc-lookahead', 15)

        sink = self.__pipeline.get_by_name('m_sink')
        sink.set_property('host', self.__host)
        sink.set_property('port', self.__port)

        self.__bus.connect('message', self.get_message)

    def close_pipeline(self):
        pass

    def get_message(self):
        message = self.__bus.timed_pop(Gst.SECOND)

        """

        if message is not None and message.type in [Gst.MessageType.EOS, Gst.MessageType.ERROR]:
            print("[VideoStreamer]: Can't stream video to server.", file=sys.stderr)

            self.__pipeline.set_state(Gst.State.NULL)
            self.__pipeline.set_state(Gst.State.PLAYING)

        if self.__tcpStatus.isUnconnected():
            self.__streamStatus.setUnconnected()
            self.__pipeline.set_state(Gst.State.NULL)

            print("[VideoStreamer]: Can't stream video to server.", file=sys.stderr)

        if self.__streamStatus.isUnconnected() and self.__tcpStatus.isConnected():
            self.__pipeline.set_state(Gst.State.PLAYING)
            self.__streamStatus.setConnected()

            print("[VideoStreamer]: re-start streaming.")

        """

        return True

    def ready(self):
        ret = self.__pipeline.set_state(Gst.State.PLAYING)

        if ret == Gst.StateChangeReturn.FAILURE:
            print("[VideoStreamer]: Failed to set pipeline state.", file=sys.stderr)

        GObject.timeout_add_seconds(3, self.get_message)

    def startPipeline(self):
        self.build_pipeline()
        self.ready()

        self.__gLoop = GObject.MainLoop()
        self.__gLoop.run()

    def on_need_data(self, src, length):
        if self.__videoBuffer.size <= 0:
            data = np.ndarray(shape=(self.__height, self.__width))
        else:
            frame = self.__videoBuffer.tail()
            data = frame.data

        data = data.tostring()

        clock = self.__pipeline.get_clock()
        #outerTimestamp = clock.get_internal_time() - self.__pipeline.get_base_time()
        outerTimestamp = self.__frameCount * self.__duration

        buffer = Gst.Buffer.new_allocate(None, len(data), None)
        buffer.fill(0, data)
        buffer.duration = self.__duration
        buffer.pts = int(outerTimestamp)
        buffer.dts = int(outerTimestamp)

        if self.__frameCount % 60 == 0:
            print("[VideoStreamer]: Attempt to send data.(timestamp: {})".format(outerTimestamp))

        retval = src.emit('push-buffer', buffer)

        if retval != Gst.FlowReturn.OK:
            print(retval)

        self.__frameCount += 1
