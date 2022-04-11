from Render.BufferMonitor import BufferMonitor

class RenderableMonitor(BufferMonitor):
    def __init__(self, name, buffer, left, top, width, height):
        super().__init__(name, buffer)

        self.__left = left
        self.__top = top
        self.__width = width
        self.__height = height

# ----------------------------------------------------------------------
# Property
# ----------------------------------------------------------------------

    @property
    def originalWidth(self):
        return self.buffer.width

    @property
    def originalHeight(self):
        return self.buffer.height

    @property
    def left(self):
        return self.__left

    @property
    def right(self):
        return self.__left + self.__width

    @property
    def top(self):
        return self.__top

    @property
    def bottom(self):
        return self.__top + self.__height

    @property
    def width(self):
        return self.__width

    @property
    def height(self):
        return self.__height

    @property
    def box(self):
        return (self.left, self.top, self.width, self.height)
