from Core.BufferHolder import BufferHolder

class BufferBroadcaster(BufferHolder):
    def __init__(self, sockets):
        super().__init__()

        self.connectBuffers(sockets)

    def push(self, value):
        for buffer in self.getBuffers():
            buffer.push(value)
