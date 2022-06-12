import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from .ControlPTZ import ControlPTZ
from .ControlPTZParser import ControlPTZParser
from .DetectionResult import DetectionResult
from .DetectionResultParser import DetectionResultParser
