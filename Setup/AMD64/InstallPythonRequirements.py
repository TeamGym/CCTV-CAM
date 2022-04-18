#!/usr/bin/env python3

import os

requirements =[
    "opencv-python",
    "numpyencoder",
    "pyglet",
    "dill",
    "pyttsx3"
]

os.system("pip3 install {}".format(' '.join(requirements)))
