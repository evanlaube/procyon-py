
from typing import Callable, Optional


class Element:
    """A parent class to base all UI elements off of. A base element draws similar
    to a label, but it is not recommended to insert a plain element into a menu
    :param label: The text to display on the element
    :type label: str
    :param refreshFunction: The function to run to refresh the label of the element
    :type refreshFunction: function
    :param color: The color to draw the text of the element in
    :type color: int, optional
    """
    def __init__(self, label : str, refreshFunction: Optional[Callable[[], str]] = None, color : int = 0):
        """Constructor method
        """
        self.label = label
        self.color = color
        self.refreshFunction = refreshFunction
        self.selectable = False
        self.isContainer = False
        self.action = None
        self.inputLocked = False

        self._width = 0
        # start maxWidth at -1 to signify element should take whole width
        self._maxWidth = -1
    
    def update(self):
        """Update the label of the element by running its refreshFunction
        """
        if self.refreshFunction == None:
            return 

        try:
            self.label = self.refreshFunction()
        except:
            raise Exception("Unable to run refreshFunction for label:", self.label)
    
    def triggerAction(self):
        """ Run the action of the element, if it exists """
        if self.action == None:
            return
        self.action()

    def sanitizeStr(self, elementStr : str):
        """ Converts a display string into a printable version, for example,
        converts tabs into four spaces """
        elementStr = elementStr.replace('\t', '    ')
        return elementStr


    def getStr(self, selected : bool = False):
        """Get the display string of the element
        :return: The text to display the element as
        :rtype: str
        """
        return self.sanitizeStr(self.label)
    
    def handleInput(self, key : int):
        """ Do nothing for now as no input should be passed into a simple element """
        pass
    
    def isInputLocked(self):
        """ Returns whether or not the cursor is locked inside the element, preventing
        navigation of elements with hjkl 
        """
        return self.inputLocked
    
    def getWidth(self):
        return self._width

    def _setWidth(self, width: int):
        if width < 1:
            raise ValueError("Cannot set width of element to zero or lower")

        self._width = width

    def getMaxWidth(self):
        return self._maxWidth
    
    def setMaxWidth(self, width: int):
        if width == 0 or width < -1:
            raise ValueError("Max width must be set to either negative one or a positive integer")
        
        self._maxWidth = width


