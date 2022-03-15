#!/usr/bin/env python3

cd ~/NeuralNetworks/darknet

mkdir weights
cd weights
wget https://github.com/AlexeyAB/darknet/releases/download/darknet_yolo_v4_pre/yolov4-tiny.weights


cd ../cfg
wget https://raw.githubusercontent.com/AlexeyAB/darknet/master/cfg/yolov4-tiny.cfg
