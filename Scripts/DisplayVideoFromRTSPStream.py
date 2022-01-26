#!/usr/bin/python3

import os
import sys
if __name__ == "__main__":
   arguments = sys.argv
   arguments.pop(0)

   rtspLocation = arguments[0]

   command = "gst-launch-1.0 rtspsrc location={} ! queue ! rtph264depay ! h264parse ! avdec_h264 ! xvimagesink"
   os.system(command.format(rtspLocation))
   

