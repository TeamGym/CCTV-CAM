from Frame import Frame

class FrameBuffer:
    def __init__(self):
        self.buffer = []

    def size(self):
        return len(self.buffer)

    def add(self, frame: Frame):
        self.buffer.append(frame)

    def remove(self, index):
        self.buffer.remove(idnex)

    def clear(self):
        self.buffer.clear()

    def get(self, index):
        return self.buffer[index]

    def pop(self, index=-1):
        return self.buffer.pop(index)
