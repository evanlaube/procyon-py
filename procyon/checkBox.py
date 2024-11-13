
from .element import Element

class CheckBox(Element):
    """This class is a UI element that works as a checkbox. It can be toggled, 
    and its current state can be easily read as either True of False"""

    def __init__(self, label, action=None, refreshFuncton=None, color=0, state=False):
        self.label = label
        self.action = action
        self.refreshFunction = refreshFuncton
        self.selectable = True
        self.color = color
        self.state = state

    
