
from enum import Enum
class UIElementType(Enum):
    NEW_LINE = 0
    EDIT = 1
    BUTTON = 2
    CHECK = 3
    COMBO = 4
    SLIDER = 5

class UIElement:
    def __init__(self, _type=None, _caption="NoCaption", _default_val=None):
        self.type = _type
        self.caption = _caption
        self.default_val = _default_val
