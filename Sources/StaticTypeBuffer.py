from Buffer import Buffer

class StaticTypeBuffer(Buffer):
    def __init__(self, elementType):
        super.__init__()

        self.__elementType = elementType

    @property
    def elementType(self):
        return self.__elementType

    def add(self, data):
        assert isinstance(data, self.__elementType), "[StaticTypeBuffer::add] Invalid type."
        
        self.rawbuffer.append(data)
