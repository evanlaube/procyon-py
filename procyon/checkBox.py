
from typing import Callable, Optional
from .element import Element

class CheckBox(Element):
    """This class is a UI element that works as a checkbox. It can be toggled, 
    and its current state can be easily read as either True of False
    :param label: The text displayed beside the checkbox
    :type label: str
    :param action: The action function to run when the checkbox is toggled
    :type action: Callable, optional 
    :param refreshFunction: A function to refresh the text of the checkbox
    :type refreshFunction: Callable, optional 
    :param color: The color to print the CheckBox in
    :type color: int, optional
    :param state: The current state of the checkbox (checked/unchecked)
    :type state: boolean
    """

    def __init__(self, label, action : Optional[Callable[[], str]] = None, 
                 refreshFuncton=None, color=0, state=False):
        super().__init__(label, refreshFunction=refreshFuncton, color=color)

        self.label = label
        self.action = action
        self.refreshFunction = refreshFuncton
        self.selectable = True
        self.color = color
        self.state = state

    def triggerAction(self):
        """ Invert the checkbox's state and run its action if it exists """
        self.state = not self.state

        if self.action is not None:
            self.action()

    def getStr(self, selected: bool = False) -> str:
        ''' Get the string the checkbox should be displayed as 
        :param selected: Whether or not the checkbox is the selected element
        :type selected: bool
        :return: String to display checkbox as
        :rtype: str
        '''
        stateChar = ' '
        if self.state:
            stateChar = '*'

        if selected:
            return f'>[{stateChar}]<{self.label}'
        else:
            return f' [{stateChar}] {self.label}'

