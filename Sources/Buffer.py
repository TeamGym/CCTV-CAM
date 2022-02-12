class Buffer:
    def __init__(self):
        self.buffer = []

    def size(self):
        return len(self.buffer)

    def add(self, data):
        self.buffer.append(data)

    def remove(self, index):
        self.buffer.remove(index)

    def clear(self):
        self.buffer.clear()

    def get(self, index):
        return self.buffer[index]

    def pop(self, index=-1):
        return self.buffer.pop(index)
