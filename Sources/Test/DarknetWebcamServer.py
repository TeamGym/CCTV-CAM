import sys

import cv2
import numpy as np

from threading import Thread

frameBuffer = []

LABELS_FILE = "Darknet/cfg/coco.names"
CONFIG_FILE = "Darknet/cfg/yolov4-tiny.cfg"
WEIGHTS_FILE= "Darknet/weights/yolov4-tiny.weights"

CONFIDENCE_THRESHOLD = 0.3

class DarknetWorker(Thread):
    def __init__(self,
                 labelFileName="Darknet/cfg/coco.names",
                 configFileName="Darknet/cfg/yolov4-tiny.cfg",
                 weightsFileName="Darknet/weights/yolov4-tiny.weights",
                 confidenceThreshold=0.3):
        super().__init__()

        self.network = cv2.dnn.readNetFromDarknet(configFileName, weightsFileName)

        layerNames = self.network.getLayerNames()
        self.layerNames = [layerNames[layer - 1] for layer in self.network.getUnconnectedOutLayers()]

        self.labels = open(labelFileName).read().strip().split("\n")
        self.colors = np.random.randint(0, 255, size=(len(self.labels), 3), dtype="uint8")

        self.confidenceThreshold = confidenceThreshold

    def run(self):
        global frameBuffer
        
        while True:
            if len(frameBuffer) == 0:
                continue

            image = frameBuffer.pop(0)
            frameBuffer.clear()

            (H, W) = image.shape[:2]

            blob = cv2.dnn.blobFromImage(image, 1 / 255.0, (416, 416), swapRB=True, crop=False)
            self.network.setInput(blob)

            layerOutputs = self.network.forward(self.layerNames)

            boxes = []
            confidences = []
            classIDs = []

            for output in layerOutputs:
                for detection in output:
                    scores = detection[5:]
                    classID = np.argmax(scores)
                    confidence = scores[classID]

                    if confidence > self.confidenceThreshold:
                        box = detection[0:4] * np.array([W, H, W, H])
                        (centerX, centerY, width, height) = box.astype("int")

                        x = int(centerX - (width / 2))
                        y = int(centerY - (height / 2))

                        boxes.append([x, y, int(width), int(height)])
                        confidences.append(float(confidence))
                        classIDs.append(classID)
                        
            idxs = cv2.dnn.NMSBoxes(boxes, confidences, self.confidenceThreshold, self.confidenceThreshold)

            if len(idxs) > 0:
                for i in idxs.flatten():
                    (x, y) = (boxes[i][0], boxes[i][1])
                    (w, h) = (boxes[i][2], boxes[i][3])

                    color = [int(c) for c in self.colors[classIDs[i]]]
                    
                    cv2.rectangle(image, (x, y), (x + w, y + h), color, 2)
                    text = "{}: {:.4f}".format(self.labels[classIDs[i]], confidences[i])
                    cv2.putText(image, text, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX,
                                0.5, color, 2)


import gi

gi.require_version('Gst', '1.0')
gi.require_version('GstRtspServer', '1.0')
from gi.repository import Gst, GstRtspServer, GObject

if __name__ == "__main__":
    class WebcamMediaFactory(GstRtspServer.RTSPMediaFactory):
        def __init__(self):
            GstRtspServer.RTSPMediaFactory.__init__(self)

            self.width = 1280
            self.height = 720
            self.fps = 10

            self.capture = cv2.VideoCapture(0)
            self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
            self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)
            self.capture.set(cv2.CAP_PROP_FPS, self.fps)
            self.duration = 1 / self.fps * Gst.SECOND
            self.frameCount = 0

            if not self.capture.isOpened():
                print("[cv2.VideoCapture]: can't open")
                sys.exit()

        def on_need_data(self, src, length):
            global frameBuffer
            
            if not self.capture.isOpened():
                return
            
            ret, frame = self.capture.read()
                
            if not ret:
                return

            frameBuffer.append(frame)

            data = frame.tostring()
            timestamp = self.frameCount * self.duration
            
            buffer = Gst.Buffer.new_allocate(None, len(data), None)
            buffer.fill(0, data)
            buffer.duration = self.duration
            buffer.pts = buffer.dts = int(timestamp)
            
            self.frameCount += 1            
            retval = src.emit('push-buffer', buffer)

            if retval != Gst.FlowReturn.OK:
                print(retval)

        def do_create_element(self, url):            
            launchString = "appsrc name=source is-live=true block=true format=GST_FORMAT_TIME" \
                           " caps=video/x-raw,width=1280,height=720,framerate=10/1,format=BGR ! videoconvert" \
                           " ! omxh264enc ! rtph264pay config-interval=1 name=pay0 pt=96"
            print(launchString)
            return Gst.parse_launch(launchString)

        def do_configure(self, rtspMedia):
            self.frameCount = 0
            
            appsrc = rtspMedia.get_element().get_child_by_name('source')
            appsrc.connect('need-data', self.on_need_data)

    class WebcamServer:
        def __init__(self):
            self.server = GstRtspServer.RTSPServer()
            self.server.set_service("3002")

            mediaFactory = WebcamMediaFactory()
            mediaFactory.set_shared(True)

            mountPoints = self.server.get_mount_points()
            mountPoints.add_factory("/webcam", mediaFactory)
            
            self.server.attach(None)

    GObject.threads_init()
    Gst.init(None)

    server = WebcamServer()

    darknetWorker = DarknetWorker()
    darknetWorker.start()
    
    gLoop = GObject.MainLoop()
    gLoop.run()

    print(1)
