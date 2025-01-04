import curses

from .container import Container
from .element import Element
from .rowBar import RowBar
from . import colors
from .keybinds import KEYBINDS

class Menu:
    """A class for storing different 'screens' of elements, as well as handling input on 
    these screens. The main purpose of this class is to easily switch between menus using
    the UIManager class
    :param name: The name of the menu
    :type name: str
    """
    def __init__(self, name : str):
        """Constructor method
        """
        self.name = name
        self.elements = {} 
        self.selectedIndex = 0
        self.scrollPadding = 2
        self._scrollPosition = 0
        self.hasSelectable = False

        self._desiredWidth : int = -1 
        self._desiredHeight : int = -1
        self._actualWidth : int = -1
        self._actualHeight = -1
        self._scalable : bool = True 

    def addElement(self, name : str, element : Element):
        """Add an element to the menu
        :param name: The name of the element
        :type name: str
        :param element: The element to add
        :type element: ui.Element
        """
        if name in self.elements.keys():
            raise Exception(f"Element with name '{name}' already exists")
        self.elements[name] = element
        if element.selectable and self.hasSelectable == False:
            self.hasSelectable = True
            self.selectedIndex = len(self.elements)-1

    def handleInput(self, key : int):
        """Forward the input key to the selected element in the menu
        :param key: The input key
        :type key: int
        """
        elementKey = list(self.elements)[self.selectedIndex]
        inputLocked = self.elements[elementKey].isInputLocked()
        if key == curses.KEY_UP or (key == ord('k') and not inputLocked): 
            if self.selectedIndex <= 0:
                return
            self.decreaseSelectedIndex()
        elif key == curses.KEY_DOWN or (key == ord('j') and not inputLocked):
            if self.selectedIndex >= len(self.elements)-1:
                return
            self.increaseSelectedIndex()
        elif key in KEYBINDS['enter']: # Enter/Return
            self.elements[elementKey].triggerAction()
        else:
            self.elements[elementKey].handleInput(key)

    def increaseSelectedIndex(self):
        """Increase the selected index of the menu, skipping unselectable elements"""
        if self.selectedIndex >= len(self.elements)-1:
            return
        self.selectedIndex += 1
        if self.selectedIndex > self._actualHeight + self._scrollPosition - 1 - self.scrollPadding:
            if self._scrollPosition < len(self.elements) - self._actualHeight:
                self._scrollPosition += 1
        while self.elements[list(self.elements)[self.selectedIndex]].selectable == False:
            self.increaseSelectedIndex()
            if(self.selectedIndex >= len(self.elements)-1):
                self.decreaseSelectedIndex()
                break

    def decreaseSelectedIndex(self):
        """Decrease the selected index of the menu, skipping unselectable elements"""
        if self.selectedIndex <= 0:
            return
        self.selectedIndex -= 1
        if self.selectedIndex < self._scrollPosition + self.scrollPadding:
            if self._scrollPosition > 0:
                self._scrollPosition -= 1
        while self.elements[list(self.elements)[self.selectedIndex]].selectable == False:
            self.decreaseSelectedIndex()
            if(self.selectedIndex <= 0):
                self.increaseSelectedIndex()
                break

    def setDesiredSize(self, width : int, height : int, resizable : bool = True):
        """ Set the desired size of the menu, otherwise it will be set to minimum
        size required to fit all elements 
        :param width: The desired width
        :type width: int
        :param height: The desired height
        :type height: int
        :param resizable: Whether or not the size of the menu can be changed or if it is fixed
        :type resizable: bool, optional 
        """
        self._desiredWidth = width
        self._desiredHeight = height
        self._scalable = resizable

    def getDesiredSize(self):
        """ Return the desired size of the menu 
        :returns: Desired size (width, height)
        :rtype: tuple
        """
        return (self._desiredWidth, self._desiredHeight)

    def setActualSize(self, width: int, height: int):
        self._actualWidth = width
        self._actualHeight = height

    def getActualSize(self):
        return (self._actualWidth, self._actualHeight)

    def isScalable(self):
        """ Returns whether or not the menu can be scaled 
        :rtype: bool
        """
        return self._scalable

    def update(self):
        """Run the update function of each element in the menu"""
        for key in self.elements.keys():
            element = self.elements[key]
            # Update element
            element.update()
            # Update width of element
            if element.getMaxWidth() == -1 or element.getWidth() > self._actualWidth:
                element._setWidth(self._actualWidth)
            elif element.getMaxWidth() < self._actualWidth:
                element._setWidth(element.getMaxWidth())

    def getScrollPosition(self):
        """
        :returns: Current vertical scroll position in menu
        :rtype: int
        """
        return self._scrollPosition
