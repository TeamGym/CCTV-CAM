import sys

from threading import Thread

from Network.VideoStreamer import VideoStreamer

import gi

gi.require_version('Gst', '1.0')
from gi.repository import Gst, GObject

class VideoStreamerThread(Thread):
    def __init__(self, streamer):
        super().__init__()

        self.streamer = streamer

    def run(self):
        self.streamer.build_pipeline()
        self.streamer.ready()

        gLoop = GObject.MainLoop()
        gLoop.run()
