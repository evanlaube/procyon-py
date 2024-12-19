

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
        
        # Start desired width and height at -1 to signify that panel should take all 
        # available space
        self._desiredWidth = -1
        self._desiredHeight = -1

        self._actualWidth = -1 
        self._actualHeight = -1 

    def getSize(self) -> tuple[int, int]:
        """
        :returns: The actual size of the panel
        :rtype: tuple[int, int]
        """
        return (self._actualWidth, self._actualHeight)

    def getDesiredSize(self) -> tuple[int, int]:
        """
        :returns: The desired size of the panel
        :rtype: tuple[int, int]
        """
        return (self._desiredWidth, self._desiredHeight)

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
        """ Set the desired size of the panel. The edges of this size cut off everything
        that tries to print outside of it. Minimum size 5x5. Note that a separator
        character is drawn along the borders of the panel
        :param width: The width to set to in characters
        :type width: int
        :param height: The height to set to in characters
        :type height: int
        """
        if (width < 5 and width != -1) or (height < 5 and height != -1):
            raise ValueError("Cannot resize Panel to a dimension less than 5. Trying to set to: ", (width, height))

        self._desiredWidth = width
        self._desiredHeight = height

        if self._desiredWidth < self._actualWidth and self._desiredWidth != -1:
            self._actualWidth = self._desiredWidth

        if self._desiredHeight < self._actualHeight and self._desiredHeight != -1:
            self._actualHeight = self._desiredHeight

    def _setActualSize(self, width: int, height: int):
        """ Sets the actual size of the panel. This method is only intended to
        be called by the UIManager class """
        if width < 5:
            raise ValueError("Panel width cannot be set smaller than 5")
        if height < 5:
            raise ValueError("Panel height cannot be set smaller than 5")

        self._actualWidth = width
        self._actualHeight = height

    def loadMenu(self, menu : Menu):
        """ Loads a menu into the panel and updates menu's size
        :param menu: The menu to load
        :type menu: Menu
        """
        self._menu = menu
        self.updateMenuSize()

    def getMenu(self):
        """
        :returns: The menu of the panel
        :rtype: Menu
        """
        return self._menu

    def updateMenuSize(self):
        """ Sets the menu to fully fill the panel, if its desired size is that big,
        otherwise, sets the menu to its desired size 
        """
        if self._menu is None:
            return

        menu = self._menu
        actWidth, actHeight = menu.getActualSize()
        desWidth, desHeight = menu.getDesiredSize()

        if self._actualWidth-1 > actWidth:
            if desWidth == -1:
                menu.setActualSize(1000, 1000)
                actWidth = self._actualWidth-1
                menu.setActualSize(actWidth, actHeight) 
            else:
                actWidth = desWidth
                menu.setActualSize(actWidth, actHeight)
                # Shrink own width
                panelWidth, panelHeight = actWidth, actHeight
                if panelWidth > 5:
                    self._setActualSize(panelWidth, self._actualHeight)
                if panelHeight > 5:
                    self._setActualSize(self._actualWidth, panelHeight)

        if self._actualHeight-1 > actHeight:
            if desHeight == -1:
                menu.setActualSize(actWidth, self._actualHeight-1)
            else:
                menu.setActualSize(actWidth, desHeight)
                # Shrink own height
                panelWidth, panelHeight = actWidth, desHeight
                if panelWidth > 5:
                    self._setActualSize(panelWidth, self._actualHeight)
                if panelHeight > 5:
                    self._setActualSize(self._actualWidth, panelHeight)
    
    def splitHorizontal(self):
        """ Split the panel into two along the horizontal axis 
        :returns: The new panels that are created with the split in format (top, bottom)
        :rtype: tuple
        """
        if self._actualWidth == -1 or self._actualHeight ==-1:
            raise Exception("Cannot split panel before its size is set")

        if self._left is not None or self._right is not None:
            raise Exception("Cannot vertically split a panel that has already been split horizontally")

        self._top = Panel(self)
        if self._menu is not None:
            self._top.loadMenu(self._menu)
        # Resize panel. If the space is not an even number, the top panel gets the extra
        # Also, remove one from the height to fit a spacer
        self._top._setActualSize(self._actualWidth, self._actualHeight // 2 + self._actualHeight %2 - 1)

        self._bottom = Panel(self)
        self._bottom._setActualSize(self._actualWidth, self._actualHeight//2)
        
        self._menu = None

        return (self._top, self._bottom)

    def splitVertical(self):
        """ Split the panel into two panels along the vertical axis 
        :returns: The new panels that are created with the split in format (left, right)
        """
        if self._actualWidth == -1 or self._actualHeight ==-1:
            raise Exception("Cannot split panel before its size is set")

        if self._top is not None or self._right is not None:
            raise Exception("Cannot horizontally split a panel that has already been split vertically")

        self._left = Panel(self)
        if self._menu is not None:
            self._left.loadMenu(self._menu)
        # Resize panel. If the space is not an even number, the left panel gets the extra
        # Remove one from the width to fit spacer
        self._left._setActualSize(self._actualWidth // 2 + self._actualWidth % 2 - 1, self._actualHeight)

        self._right = Panel(self)
        self._right._setActualSize(self._actualWidth//2, self._actualHeight)

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
