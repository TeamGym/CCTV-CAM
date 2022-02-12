from FrameBuffer import FrameBuffer
from DetectionResultBuffer import DetectionResultBuffer

from ServerConfig import ServerConfig

from RtspServerThread import RtspServerThread
from DetectionThread import DetectionThread

if __name__ == "__main__":
    frameBuffer = FrameBuffer()
    detectionResultBuffer = DetectionResultBuffer()

    serverConfig = ServerConfig()
    serverConfig.loadFromConfigFile("ServerConfig.ini")

    rtspServerThread = RtspServerThread(frameBuffer, serverConfig)

    labelFileName = "Darknet/cfg/coco.names"
    configFileName = "Darknet/cfg/yolov4-tiny.cfg"
    weightsFileName = "Darknet/weights/yolov4-tiny.weights"

    confidenceThreshold = 0.3

    detectionThread = DetectionThread(
        labelFileName,
        configFileName,
        weightsFileName,
        confidenceThreshold,
        frameBuffer,
        detectionResultBuffer)

    rtspServerThread.start()
