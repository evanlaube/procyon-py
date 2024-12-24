
from .element import Element

import curses
import curses.ascii
from typing import Callable, Optional
from .keybinds import KEYBINDS

class TextField(Element):
    """This class is a UI element that works as a one-line text field. Some
    examples of use cases include search fields, and username/password fields.
    :param label: The text displayed left of the input
    :type label: str
    :param action: Action function to run when enter is pressed
    :type action: Callable, optional
    :param refreshFunction: A function to refresh the text of the text field
    :type refreshFunction: Callable, optional
    :param color: The color to display the searchfield in
    :type color: int, optional
    :param value: The starting value of the text field
    :type value: str 
    :param minWidth: The minimum width that the text field will draw with
    :type minWidth: int
    """

    def __init__(self, label, action : Optional[Callable[[], str]] = None,
                 refreshFunction=None, color : int = 0, value : str = '') :
        """Constructor method"""
        color = color | curses.A_UNDERLINE
        super().__init__(label, refreshFunction=refreshFunction, color=color)
        self.action = action
        self.selectable = True
        self.value = value
        self.inputLocked = True

        # Make text fields not take up whole width by default
        self._maxWidth = 40

    def getStr(self, selected: bool = False) -> str:
        """ Get the string the text field should display as in the menu
        :param selected: Whether the textField is selected 
        :type selected: bool 
        :return: String to display checkbox as 
        :rtype: str
        """

        promptWidth = len(self.label) + 3
        valueWidth = self._width - promptWidth

        if promptWidth + len(self.value) > self._width:
            valueStr = self.value[len(self.value) - valueWidth:]
        else:
            valueStr = self.value

        string = f' {self.label}: {valueStr}'
        if selected:
            string = '>' + string[1:]

        string = string.ljust(self._width)

        return self.sanitizeStr(string)


    def handleInput(self, key : int):
        """ Add the input character to the text field if it is a valid character"""
        # If key is backspace of mac delete remove last character of value
        if key in KEYBINDS['backspace']:
            self.value = self.value[:len(self.value)-1]
        if key in KEYBINDS['backspaceWord']:
            while len(self.value) != 0 and self.value[-1] != ' ':
                self.value = self.value[:len(self.value)-1]
            self.value = self.value[:len(self.value)-1]

        elif curses.ascii.isprint(key):
            self.value += chr(key)
