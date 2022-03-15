#!/usr/bin/env python3

import os

requirements =[
    "opencv-cuda",
    "cudnn",
    "gst-rtsp-server",
    "vtk",
    "hdf5",
    "glew",
    "jsoncpp",
    "pugixml",
    "fmt"
]
print(' '.join(requirements))
os.system("sudo pacman -S {}".format(' '.join(requirements)))
