

from procyon.menu import Menu


class Panel:
    """A class that can be used to structure the UI into different split sections.
    A Panel either is a leaf and displays a menu, or contains other panels. Note that
    a separator character is drawn along the borders where two panels are connected 
    :param parent: The panel that contains the new panel
    :type parent: Panel
    """
    def __init__(self, parent = None):
        """ Constructor method """
        self._menu : Menu | None = None
        # Store references to potential split panels. Note that only either top and bottom
        # or left and right can be defined. A panel can only be split in two 
        self._top : Panel | None = None
        self._bottom : Panel | None = None
        self._left : Panel | None = None
        self._right : Panel | None = None 

        # Store a reference to the parent of the panel for easy traversal
        self._parent : Panel | None = parent 
        
        # Start width and height as -1, signifying the panel should use all available space
        self._width = -1 
        self._height = -1 

    def getSize(self) -> tuple[int, int]:
        """
        :returns: The size of the panel
        :rtype: tuple[int, int]
        """
        return (self._width, self._height)

    def getLeft(self):
        return self._left

    def getRight(self):
        return self._right

    def getTop(self):
        return self._top

    def getBottom(self):
        return self._bottom

    def getParent(self):
        return self._parent

    def setSize(self, width: int, height: int):
        """ Set the size of the panel. The edges of this size cut off everything
        that tries to print outside of it. Minimum size 5x5. Note that a separator
        character is drawn along the borders of the panel
        :param width: The width to set to in characters
        :type width: int
        :param height: The height to set to in characters
        :type height: int
        """
        if width < 5 or height < 5:
            raise ValueError("Cannot resize Panel to a dimension less than 5")

        self._width = width
        self._height = height

    def loadMenu(self, menu : Menu):
        """ Loads a menu into the panel 
        :param menu: The menu to load
        :type menu: Menu
        """
        self._menu = menu

    def getMenu(self):
        """
        :returns: The menu of the panel
        :rtype: Menu
        """
        return self._menu
    
    def splitHorizontal(self):
        """ Split the panel into two along the horizontal axis 
        :returns: The new panels that are created with the split in format (top, bottom)
        :rtype: tuple
        """
        if self._width == -1 or self._height ==-1:
            raise Exception("Cannot split panel before its size is set")

        if self._left is not None or self._right is not None:
            raise Exception("Cannot vertically split a panel that has already been split horizontally")

        self._top = Panel(self)
        if self._menu is not None:
            self._top.loadMenu(self._menu)
        # Resize panel. If the space is not an even number, the top panel gets the extra
        # Also, remove one from the height to fit a spacer
        self._top.setSize(self._width, self._height // 2 + self._height %2 - 1)

        self._bottom = Panel(self)
        self._bottom.setSize(self._width, self._height//2)
        
        self._menu = None

        return (self._top, self._bottom)

    def splitVertical(self):
        """ Split the panel into two panels along the vertical axis 
        :returns: The new panels that are created with the split in format (left, right)
        """
        if self._width == -1 or self._height ==-1:
            raise Exception("Cannot split panel before its size is set")

        if self._top is not None or self._right is not None:
            raise Exception("Cannot horizontally split a panel that has already been split vertically")

        self._left = Panel(self)
        if self._menu is not None:
            self._left.loadMenu(self._menu)
        # Resize panel. If the space is not an even number, the left panel gets the extra
        # Remove one from the width to fit spacer
        self._left.setSize(self._width // 2 + self._width % 2 - 1, self._height)

        self._right = Panel(self)
        self._right.setSize(self._width//2, self._height)

        self._menu = None

        return (self._left, self._right) 

    def isSelectable(self):
        """ Returns whether or not the panel either contains a menu with a selectable 
        element, or contains another panel that is selectable 
        :returns: Whether or not the panel is selectable
        :rtype: bool
        """
        if self._menu is not None:
            return self._menu.hasSelectable
        else:
            if self._left is not None and self._left.isSelectable():
                return True
            elif self._top is not None and self._top.isSelectable():
                return True
            elif self._right is not None and self._right.isSelectable():
                return True
            elif self._bottom is not None and self._bottom.isSelectable():
                return True
        return False
    
    def hasMenu(self):
        """ Returns whether the panel directly contains a menu, making it a
        leaf panel 
        """
        return self._menu is not None
