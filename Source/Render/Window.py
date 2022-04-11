import pyglet
from pyglet.gl import *
import ctypes

class Window(pyglet.window.Window):
    def __init__(self, width, height, fps):
        self.__eventHandlers = {
            "KeyDown": [],
            "KeyUp": [],
            "KeyPress": [],
            "MouseDown": [],
            "MouseUp": [],
            "MousePress": [],
            "MouseMove": [],
            "MouseDrag": []
        }

        self.__keyState = {}
        self.__buttonState = {}

        self.__mouseX = 0
        self.__mouseY = 0

        super().__init__(width=width, height=height)

        pyglet.clock.schedule_interval(self.update, 1.0 / fps)

# ----------------------------------------------------------------------
# Private Member Method
# ----------------------------------------------------------------------

    def __setMousePosition(self, x, y):
        self.__mouseX = x
        self.__mouseY = y

    def __getEventHandlers(self, eventType):
        return self.__eventHandlers[eventType]

    def __getPressedButton(self):
        for button in self.__buttonState:
            if self.__buttonState[button]:
                return button

        return -1

# ----------------------------------------------------------------------
# Property
# ----------------------------------------------------------------------

    @property
    def width(self):
        return self.get_size()[0]

    @width.setter
    def width(self, value):
        self.set_size(value, self.height)

    @property
    def height(self):
        return self.get_size()[1]

    @height.setter
    def height(self, value):
        self.set_size(self.width, value)

    @property
    def size(self):
        return self.get_size()

    @size.setter
    def size(self, value):
        self.set_size(value)

# ----------------------------------------------------------------------
# Public Member Method
# ----------------------------------------------------------------------

    def update(self, deltaTime):
        for key in self.__keyState:
            if self.__keyState[key]:
                for handler in self.__getEventHandlers("KeyPress"):
                    handler(key)

        for button in self.__buttonState:
            if self.__buttonState[button]:
                for handler in self.__getEventHandlers("MousePress"):
                    handler(self.__mouseX, self.__mouseY, button)

# ----------------------------------------------------------------------
# Event Handler
# ----------------------------------------------------------------------

    def addEventHandler(self, eventType, handler):
        self.__eventHandlers[eventType].append(handler)

    def removeEventHandler(self, eventType, handler):
        self.__eventHandlers[eventType].remove(handler)

    def on_key_press(self, symbol, modifiers):
        for handler in self.__getEventHandlers("KeyDown"):
            handler(symbol)

        self.__keyState[symbol] = True

    def on_key_release(self, symbol, modifiers):
        for handler in self.__getEventHandlers("KeyUp"):
            handler(symbol)

        self.__keyState[symbol] = False

    def on_mouse_press(self, x, y, button, modifiers):
        for handler in self.__getEventHandlers("MouseDown"):
            handler(x, y, button)

        self.__setMousePosition(x, y)
        self.__buttonState[button] = True

    def on_mouse_release(self, x, y, button, modifiers):
        for handler in self.__getEventHandlers("MouseUp"):
            handler(x, y, button)

        self.__setMousePosition(x, y)
        self.__buttonState[button] = False

    def on_mouse_motion(self, x, y, dx, dy):
        for handler in self.__getEventHandlers("MouseMove"):
            handler(x, y, dx, dy)

        self.__setMousePosition(x, y)

    def on_mouse_drag(self, x, y, dx, dy, button, modifiers):
        for handler in self.__getEventHandlers("MouseDrag"):
            handler(x, y, dx, dy, button)

        self.__setMousePosition(x, y)
