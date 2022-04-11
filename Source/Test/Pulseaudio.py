import pulsectl

class AudioDeviceController:
    def __init__(self):
        self.__pulse = pulsectl.Pulse('AudioDeviceController')

        self.__volumeStep = 0.05

# ----------------------------------------------------------------------
# Private Method
# ----------------------------------------------------------------------

    def __checkVolumeInput(self, value):
        assert value >= 0 and value <= 1.0

    def __getSinkList(self):
        return self.__pulse.sink_list()

    def __forEachSink(self, func):
        for sink in self.__getSinkList():
            func(sink)

# ----------------------------------------------------------------------
# Property
# ----------------------------------------------------------------------

    @property
    def volumeStep(self):
        return self.__volumeStep

    @volumeStep.setter
    def volumeStep(self, value):
        self.__checkVolumeInput(value)

        self.__volumeStemp = value

# ----------------------------------------------------------------------
# Volume
# ----------------------------------------------------------------------

    def getMaxVolume(self):
        return max(self.getVolumes())

    def getMinVolume(self):
        return min(self.getVolumes())

    def getVolumes(self):
        sinks = self.__getSinkList()
        return [self.__pulse.volume_get_all_chans(sink) for sink in sinks]

    def setVolume(self, value):
        self.__checkVolumeInput(value)

        self.__pulse.set_all_chans(value)

    def changeVolume(self, value=0.05):
        for sink in self.__getSinkList():
            self.__pulse.volume_change_all_chans(sink, value)

    def increaseVolume(self):
        for sink in self.__getSinkList():
            self.__pulse.volume_change_all_chans(sink, self.__volumeStep)

    def decreaseVolume(self):
        for sink in self.__getSinkList():
            self.__pulse.volume_change_all_chans(sink, -self.__volumeStep)

# ----------------------------------------------------------------------
# Mute
# ----------------------------------------------------------------------

    def mute(self):
        for sink in self.__getSinkList():
            self.__pulse.mute(sink, True)

    def unmute(self):
        for sink in self.__getSinkList():
            self.__pulse.mute(sink, False)

c = AudioDeviceController()
