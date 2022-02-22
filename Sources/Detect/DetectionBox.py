class DetectionBox:
    def __init__(self,
                 x : int,
                 y : int,
                 width : int,
                 height : int,
                 confidence : float,
                 classID : int,
                 label : str):
        self.__x = x
        self.__y = y
        self.__width = width
        self.__height = height
        
        self.__left = x
        self.__right = x + width
        self.__top = y
        self.__bottom = y + height

        self.__confidence = confidence
        self.__classID = classID
        self.__label = label

    def as_dict(self):
        return {
            'x': self.x,
            'y': self.y,
            'width': self.width,
            'height': self.height,
            'left': self.left,
            'right': self.right,
            'top': self.top,
            'bottom': self.bottom,
            'confidence': self.confidence,
            'label': self.label
        }

    @property
    def x(self):
        return self.__x

    @x.setter
    def x(self, value):
        self.__x = value

    @property
    def y(self):
        return self.__y

    @y.setter
    def y(self, value):
        self.__y = value

    @property
    def width(self):
        return self.__width

    @width.setter
    def width(self, value):
        self.__width = value

    @property
    def height(self):
        return self.__height

    @height.setter
    def height(self, value):
        self.__height = value

    @property
    def left(self):
        return self.__x

    @property
    def right(self):
        return self.__x + self.__width

    @property
    def top(self):
        return self.__y

    @property
    def bottom(self):
        return self.__y + self.__height

    @property
    def confidence(self):
        return self.__confidence

    @confidence.setter
    def confidence(self, value):
        self.__confidence = value

    @property
    def classID(self):
        return self.__classID

    @classID.setter
    def classID(self, value):
        self.__classID = value

    @property
    def label(self):
        return self.__label

    @label.setter
    def label(self, value):
        self.__label = value
