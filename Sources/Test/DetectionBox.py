class DetectionBox:
    def __init__(self,
                 x : int,
                 y : int,
                 width : int,
                 height : int,
                 confidence : float,
                 classID : int,
                 label : str):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        
        self.left = x
        self.right = x + width
        self.top = y
        self.bottom = y + height

        self.confidence = confidence
        self.classID = classID
        self.label = label
