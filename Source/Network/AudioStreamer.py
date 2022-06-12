import time
import sys
import numpy as np

import gi

gi.require_version('Gst', '1.0')
from gi.repository import Gst, GObject

from Network import ServerStatus
from Thread import ThreadRunner

class AudioStreamer(ThreadRunner):
    def __init__(self, host, port):
        super().__init__(func=self.startPipeline)

        self.__host = host
        self.__port = port

        self.__pipeline = None

        GObject.threads_init()
        Gst.init(None)

    @property
    def pipeline(self):
        return self.__pipeline

    def build_pipeline(self):
        self.__pipeline = Gst.parse_launch(
            "alsasrc device=\"hw:0\" name=m_src ! "
            "mulawenc name=m_encoder ! rtppcmupay ! udpsink name=m_sink")
        self.__bus = self.__pipeline.get_bus()

        source = self.__pipeline.get_by_name('m_src')
        encoder = self.__pipeline.get_by_name('m_encoder')

        sink = self.__pipeline.get_by_name('m_sink')
        sink.set_property('host', self.__host)
        sink.set_property('port', self.__port)

    def close_pipeline(self):
        pass

    def ready(self):
        ret = self.__pipeline.set_state(Gst.State.PLAYING)

        if ret == Gst.StateChangeReturn.FAILURE:
            print("[VideoStreamer]: Failed to set pipeline state.", file=sys.stderr)

    def startPipeline(self):
        self.build_pipeline()
        self.ready()

        self.__gLoop = GObject.MainLoop()
        self.__gLoop.run()
