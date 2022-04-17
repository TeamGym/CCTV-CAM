import os
import sys

class DeviceFinder:
    def findCameraByName(self):
        v4l2Result = os.popen("v4l2-ctl --list-device").read()
        pass
