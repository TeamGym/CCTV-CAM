#!/usr/bin/env python3

import os

requirements =[
    "espeak"
]

os.system("yay -S {}".format(' '.join(requirements)))
