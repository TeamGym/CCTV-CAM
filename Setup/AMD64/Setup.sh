#!/usr/bin/env bash

./InstallPacmanRequirements.py
sudo ln -s /opt/cuda /usr/local/cuda

curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py

./InstallPythonRequirements.py

git clone https://github.com/pjreddie/darknet ~/NeuralNetworks/darknet
cd ~/NeuralNetworks/darknet

# GPU=1
# CUDNN=1
# OPENCV=1
# opencv -> opencv4
# ARCH = -gencode arch=compute_86,code=[sm_86,compute_86]
emacs Makefile

wget https://gist.githubusercontent.com/tiagoshibata/f322466e8b31c14a4b98d53bf74e4f6c/raw/ffe8077274e14f400a9d53f79aedb4ba4b7abe89/darknet-fix-opencv-4.patch
patch -p1 < darknet-fix-opencv-4.patch 

make

./DownloadYolov4Tiny.py
