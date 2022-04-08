class RemoteDeviceController:
    def __init__(self, context):
        self.__commandQueue = context.commandQueue
        self.__audioDeviceController = context.audioDeviceController
        self.__cameraDeviceController = context.cameraDeviceController
