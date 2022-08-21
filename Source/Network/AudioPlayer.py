import sys
import gi

gi.require_version('Gst', '1.0')
from gi.repository import Gst, GObject

from Thread import ThreadRunner

class AudioPlayer(ThreadRunner):
    def __init__(self, port):
        super().__init__(func=self.startPipeline)

        self.__port = port

        self.__pipeline = None

        GObject.threads_init()
        Gst.init(None)

    @property
    def pipeline(self):
        return self.__pipeline

    def build_pipeline(self):
        self.__pipeline = Gst.parse_launch(
            "udpsrc port={} ! audio/x-raw,channels=2,rate=48000,format=S16LE,layout=interleaved ! audioconvert ! autoaudiosink sync=false"
        .format(self.__port))
        self.__bus = self.__pipeline.get_bus()

        source = self.__pipeline.get_by_name('m_src')

    def get_message(self):
        message = self.__bus.timed_pop(Gst.SECOND)

        print(message.type)
        return True

    def close_pipeline(self):
        pass

    def ready(self):
        ret = self.__pipeline.set_state(Gst.State.PLAYING)

        if ret == Gst.StateChangeReturn.FAILURE:
            print("[AudioPlayer]: Failed to set pipeline state.", file=sys.stderr)

    def startPipeline(self):
        self.build_pipeline()
        self.ready()

        self.__gLoop = GObject.MainLoop()
        self.__gLoop.run()
