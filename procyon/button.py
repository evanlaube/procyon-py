
from .element import Element
from typing import Callable, Optional

class Button(Element):
    """This class is a UI element that works as a button. It can be selected, and
    an action can be acttached to it that is triggered when the button is activated.
    :param label: The text displayed inside the button
    :type label: str
    :param action: The action that the button activates
    :type action: function 
    :param refreshFunction: Function to refresh the label text on update
    :type refreshFunction: function, optional
    :param color: The text color to draw the element with
    :type color: int, optional
    :param setLabelToResult: Whether or not to set the label of the button to the 
    :return value of its action function
    :type setLabelToResult: bool, optional
    """

    def __init__(self, label : str, action : Callable, refreshFunction : Optional[Callable[[], str]] = None, 
                 color : int =0, setLabelToResult : bool = False):
        """Constructor method
        """
        super().__init__(label, refreshFunction=refreshFunction, color=color)
        self.action = action
        self.selectable = True
        self.setLabelToResult = setLabelToResult

    def triggerAction(self):
        """Run the button's action function"""
        result = self.action()
        if type(result) == str and self.setLabelToResult:
            self.label = str(result)

    def getStr(self, selected : bool =False) -> str:
        """Get the string that the button should display as
        :param selected: Whether or not the button is selected in the menu
        :type selected: bool, optional
        """
        elementStr = ""
        if selected:
            elementStr = '[>' + self.label + '<]'
        else:
            elementStr = '[ ' + self.label + ' ]'

        return self.sanitizeStr(elementStr)
