import curses

from .keybinds import KEYBINDS 
from .panel import Panel

from .menu import Menu

class UIManager:
    """A class for managing and running all UI functions. The UIManager stores a dict of
    menus to easily switch between them, and passes keyboard inputs to the selected menu only,
    as well as updating the menu
    :param stdscr: The screen to print menus to
    """
    def __init__(self, stdscr : curses.window):
        """ Constructor method """
        self.stdscr = stdscr
        self.shouldExit = False

        self._rootPanel : Panel = Panel()
        self._selectedPanel : Panel = self._rootPanel
        self.rows, self.cols = self.stdscr.getmaxyx()

        # Create a root panel to contain all other panels
        # Make root panel fill window
        self._rootPanel._setActualSize(self.cols, self.rows)

        # Create a dictionary to store menus
        self._menus = {}

        curses.curs_set(0)
        curses.noecho()

        self.initializeColors()

        self.stdscr.bkgd(' ', curses.color_pair(0))
        self.stdscr.clear()
        self.stdscr.refresh()
        self.stdscr.timeout(100)

        # Use alternate screen buffer to prevent scrollback trail
        curses.raw() 
        self.stdscr.leaveok(True)

    def initializeColors(self):
        """ Initializes the curses color pairs """
        curses.start_color()
        curses.use_default_colors()

        # Background color pallette (XTerm-256)
        bgColors = [-1,0,1,2,3,4,5,6,236]

        try:
            for i in range(len(bgColors)):
                for n in range(16):
                    curses.init_pair(i*16+n, n-1, bgColors[i])
        except:
            # Return for now. TODO: find a way to enter single color mode
            return

    def updateWindowSize(self):
        ''' Gets the current size of the curses window and stores it in member
        variables self.rows and self.cols'''
        self.rows, self.cols = self.stdscr.getmaxyx()
        # Subtract one from cols to prevent error when printing in bottom right corner
        self.cols -= 1

        self._updatePanelSize(self._rootPanel, self.rows, self.cols)

    def _updatePanelSize(self, panel : Panel, rows : int, cols : int):
        panel._setActualSize(cols, rows)

        left = panel.getLeft()
        right = panel.getRight()
        top = panel.getTop()
        bottom = panel.getBottom()
        
        if left is not None and right is not None:
            leftMenu = left.getMenu()
            rightMenu = right.getMenu()

            leftDesiredWidth = rightDesiredWidth = -1

            if leftMenu is not None:
                leftDesiredWidth = leftMenu.getDesiredSize()[0]

            if rightMenu is not None:
                rightDesiredWidth = rightMenu.getDesiredSize()[0]

            if leftDesiredWidth == -1 and rightDesiredWidth == -1:
                leftCols = cols // 2 
                rightCols = cols - leftCols
            elif leftDesiredWidth == -1:
                rightCols = min(rightDesiredWidth, cols-5)
                leftCols = cols - rightCols
            elif rightDesiredWidth == -1:
                leftCols = min(leftDesiredWidth, cols-5)
                rightCols = cols - leftCols
            else:
                # Split 50/50 for now
                # TODO: Implement logic here
                leftCols = cols // 2 
                rightCols = cols - leftCols

            if leftMenu is not None:
                leftMenu.setActualSize(leftCols-1, rows-1)

            if rightMenu is not None:
                rightMenu.setActualSize(rightCols-1, rows-1)

            self._updatePanelSize(right, rows, rightCols)
            self._updatePanelSize(left, rows, leftCols)
        elif top is not None and bottom is not None:
            topMenu = top.getMenu()
            bottomMenu = bottom.getMenu()

            topDesiredHeight = bottomDesiredHeight = -1

            if topMenu is not None:
                topDesiredHeight = topMenu.getDesiredSize()[1]

            if bottomMenu is not None:
                bottomDesiredHeight = bottomMenu.getDesiredSize()[1]

            if topDesiredHeight == -1 and bottomDesiredHeight == -1:
                topRows = rows // 2 
                bottomRows = rows - topRows 
            elif bottomDesiredHeight == -1:
                topRows = min(topDesiredHeight, rows-5)
                bottomRows = rows - topRows
            elif topDesiredHeight == -1:
                bottomRows = min(bottomDesiredHeight, rows-5)
                topRows = rows - bottomRows
            else:
                # Split 50/50 for now
                # TODO: Implement logic here
                topRows = rows // 2 
                bottomRows = rows - topRows 

            if topMenu is not None:
                topMenu.setActualSize(cols, topRows)

            if bottomMenu is not None:
                bottomMenu.setActualSize(cols, bottomRows)

            self._updatePanelSize(top, topRows, cols)
            self._updatePanelSize(bottom, bottomRows, cols)

    def run(self):
        """Reset the current display and run the main loop"""
        self.mainLoop()
        self.cleanup()

    def cleanup(self):
        """Reset terminal state before exiting"""
        curses.nocbreak()
        self.stdscr.keypad(False)
        curses.echo()
        curses.endwin() 

    def display(self):
        """ Displays the root panel """
        if self._rootPanel is not None:
           self.stdscr.clear()
           self._recDisplayPanel(self._rootPanel, (0,0))

    def _recDisplayPanel(self, panel : Panel | None, position : tuple[int, int]):
        """ Recursively display all panels and update their menus 
        :param panel: The current panel to display
        :type panel: Panel
        :param position: The position on the screen to draw the top left of the panel
        :type position: tuple[int, int]
        """
        if panel is None:
            return

        menu = panel.getMenu()
        # If the panel doesn't have a menu, draw separators along its borders
        # along other panels
        if menu is None:
            verticalSep = '│'
            horizontalSep = '─'
            intersection = '┼'
            #TODO: Find a way to print intersections of separators
            top = panel.getTop()
            bottom = panel.getBottom()
            left = panel.getLeft()
            right = panel.getRight()
            if top is not None and bottom is not None:
                topSize = top.getSize()

                self._recDisplayPanel(panel.getTop(), position)
                self._recDisplayPanel(panel.getBottom(), (position[0], position[1] + topSize[1]))
                try:
                    for x in range(position[0], position[0] + topSize[0]):
                        self.stdscr.addstr(position[1]+topSize[1], position[0] + x, horizontalSep)
                except:
                    return
            elif left is not None and right is not None:
                leftSize = left.getSize()

                self._recDisplayPanel(panel.getLeft(), position)
                self._recDisplayPanel(panel.getRight(), (position[0]+leftSize[0]+1, position[1]))
                
                try:
                    for y in range(position[1], position[1] + leftSize[1] + 1): # TODO: Figure out this +1
                        self.stdscr.addstr(y, position[0]+leftSize[0], verticalSep) 
                except:
                    return
        else:
            self._displayLeafPanel(panel, position)

    def _displayLeafPanel(self, panel : Panel, position : tuple[int, int]):
        """ Displays a panel that contains a menu """
        menu = panel.getMenu()
        if menu is None:
            return
 
        # TODO: Figure out how to determine if panel is selceted
        panelSelected = panel == self._selectedPanel 
 
        # Display Menu
        scrollPos = menu.getScrollPosition()
        elements = menu.elements
        startY = position[1]
        startX = position[0]

        # Hacky fix, but for now this works to prevent drawing first line of bottom
        # panel on border
        parent = panel.getParent()
        if parent is not None:
            if panel is parent.getBottom():
                startY += 1
        
        elementList = list(elements.values())
        lines = []
        for id in range(scrollPos, len(elementList)):
            selected = panelSelected & (id == (menu.selectedIndex))
            lines += elementList[id].getStr(selected).split('\n')

        for y in range(len(lines)):
            if y >= panel.getSize()[1]:
                return

            line = lines[y]
            if len(line) > panel.getSize()[0]:
                line = line[0:panel.getSize()[0]]
            try:
                self.stdscr.addstr(y + startY, startX, line)
            except:
                pass

    def update(self):
        """ Updates each individual panel """
        if self._rootPanel is not None:
            self._recUpdatePanel(self._rootPanel)

    def _recUpdatePanel(self, panel : Panel | None):
        """ Recursive call for update method """
        if panel is None:
            return

        # Update panel menus
        menu = panel.getMenu()
        if menu is not None:
            menu.update()
            return

        if panel.getTop() and panel.getBottom():
            # If panel is split vertically
            top = panel.getTop()
            bottom = panel.getBottom()

            if top is None or bottom is None:
                raise Exception("Panels undefined")

            height = panel.getSize()[1]
            width = panel.getSize()[0]
            extraHeight = height - (top.getSize()[1] + bottom.getSize()[1])

            topHeight = top.getSize()[1]
            bottomHeight = bottom.getSize()[1] 

            if extraHeight != 0:
                topDesiredHeight = top.getDesiredSize()[1]
                bottomDesiredHeight = bottom.getDesiredSize()[1]

                if topDesiredHeight == -1 and bottomDesiredHeight == -1:
                    topHeight = height // 2
                    bottomHeight = height - topHeight
                elif topDesiredHeight == -1 and bottomDesiredHeight != -1:
                    bottomHeight = min(height-10, bottomDesiredHeight)
                    topHeight = height-bottomHeight
                elif topDesiredHeight != -1 and bottomDesiredHeight == -1:
                    topHeight = min(height-10, topDesiredHeight)
                    bottomHeight = height-topHeight
                else:
                    extraHeight = height - (topDesiredHeight + bottomDesiredHeight)
                    if extraHeight > 0:
                        topHeight = topDesiredHeight
                        bottomHeight = bottomDesiredHeight
                    else:
                        if topDesiredHeight < height // 2:
                            topHeight = topDesiredHeight
                            bottomHeight = height - topHeight
                        elif bottomDesiredHeight < height // 2:
                            bottomHeight = bottomDesiredHeight
                            topHeight = height - bottomHeight
                        else:
                            topHeight = height // 2
                            bottomHeight = height - topHeight 

            topWidth = min(top.getDesiredSize()[0], width)
            bottomWidth = min(bottom.getDesiredSize()[0], width)

            if topWidth == -1:
                topWidth = width 

            if bottomWidth == -1:
                bottomWidth = width 

        if panel.getLeft() and panel.getRight():
            # If panel split horizontally
            left = panel.getLeft()
            right = panel.getRight()

            if left is None or right is None:
                raise Exception("Panels undefined")

            width = panel.getSize()[0]
            height = panel.getSize()[1]
            extraWidth = width - (left.getSize()[0] + right.getSize()[0])

            leftWidth = left.getSize()[0]
            rightWidth = right.getSize()[0] 
            
            if extraWidth != 0:
                leftDesiredWidth = left.getDesiredSize()[0]
                rightDesiredWidth = right.getDesiredSize()[0]

                if leftDesiredWidth == -1 and rightDesiredWidth == -1:
                    leftWidth = width // 2
                    rightWidth = width - leftWidth
                elif leftDesiredWidth == -1 and rightDesiredWidth != -1:
                    rightWidth = min(width-10, rightDesiredWidth)
                    leftWidth = width - rightWidth
                elif leftDesiredWidth != -1 and rightDesiredWidth == -1:
                    leftWidth = min(width-10, leftDesiredWidth)
                    rightWidth = width - leftWidth
                else:
                    extraWidth = width - (leftDesiredWidth + rightDesiredWidth)
                    if extraWidth > 0:
                        leftWidth = leftDesiredWidth
                        rightWidth = rightDesiredWidth
                    else:
                        if leftDesiredWidth < width // 2:
                            leftWidth = leftDesiredWidth
                            rightWidth = width - leftWidth
                        elif rightDesiredWidth < width // 2:
                            rightWidth = rightDesiredWidth
                            leftWidth = width - rightWidth
                        else:
                            leftWidth = width // 2
                            rightWidth = width - leftWidth

            rightHeight = min(right.getDesiredSize()[1], height)
            leftHeight = min(left.getDesiredSize()[1], height)

            if leftHeight == -1:
                leftHeight = height
            if rightHeight == -1:
                rightHeight = height

            if leftWidth == 0:
                raise Exception(f"LeftWidth is zero! leftSize:{left.getSize()} leftDesiredSize:{left.getDesiredSize()} rightSize:{right.getSize()} rightDesiredSize:{right.getDesiredSize()}")

        self._recUpdatePanel(panel.getLeft())
        self._recUpdatePanel(panel.getRight())
        self._recUpdatePanel(panel.getTop())
        self._recUpdatePanel(panel.getBottom())

    def selectPanel(self, panel : Panel):
        """ Searches the given panel for a panel with a menu in it and selects
        the first one found. Search order is top, left, bottom, right. 
        :param panel: The panel to select
        :type panel: Panel
        """
        if panel.hasMenu():
            self._selectedPanel = panel
            return

        top = panel.getTop()
        right = panel.getRight()
        bottom = panel.getBottom()
        left = panel.getLeft()

        # Carry out traversal order in reverse
        if right is not None:
            self.selectPanel(right)
        if bottom is not None:
            self.selectPanel(bottom)
        if left is not None:
            self.selectPanel(left)
        if top is not None:
            self.selectPanel(top)

    def _findLeftmostPanel(self, candidate : Panel, fromPanel : Panel):
        if candidate.hasMenu():
            return candidate

        left, right = candidate.getLeft(), candidate.getRight()

        if left is not None and right is not None:
            return self._findLeftmostPanel(left, fromPanel)

        top, bottom = candidate.getTop(), candidate.getBottom()
        if top is not None and bottom is not None:
            parent = fromPanel.getParent()

            if parent is not None and parent.getTop() == fromPanel:
                return self._findLeftmostPanel(top, fromPanel)
            else:
                return self._findLeftmostPanel(bottom, fromPanel)

        return candidate
    
    def _findRightmostPanel(self, candidate : Panel, fromPanel : Panel):
        if candidate.hasMenu():
            return candidate
        
        left, right = candidate.getLeft(), candidate.getRight()
        if left is not None and right is not None:
            return self._findRightmostPanel(right, fromPanel)

        top, bottom = candidate.getTop(), candidate.getBottom()
        if top is not None and bottom is not None:
            parent = fromPanel.getParent()
            if parent is not None and parent.getBottom() == fromPanel:
                return self._findRightmostPanel(bottom, fromPanel)
            else:
                return self._findRightmostPanel(top, fromPanel)

        return candidate

    def _findTopmostPanel(self, candidate : Panel, fromPanel : Panel):
        if candidate.hasMenu():
            return candidate

        top, bottom = candidate.getTop(), candidate.getBottom()
        if top is not None and bottom is not None:
            return self._findTopmostPanel(top, fromPanel)
        
        left, right = candidate.getLeft(), candidate.getRight()
        if left is not None and right is not None:
            parent = fromPanel.getParent()
            if parent is not None and parent.getRight() == fromPanel:
                return self._findTopmostPanel(right, fromPanel)
            else:
                return self._findTopmostPanel(left, fromPanel)

        return candidate

    def _findBottommostPanel(self, candidate : Panel, fromPanel : Panel):
        if candidate.hasMenu():
            return candidate

        top, bottom = candidate.getTop(), candidate.getBottom()
        if top is not None and bottom is not None:
            return self._findBottommostPanel(bottom, fromPanel)

        left, right = candidate.getLeft(), candidate.getRight()
        if left is not None and right is not None:
            parent = fromPanel.getParent()
            if parent is not None and parent.getLeft() == fromPanel:
                return self._findBottommostPanel(left, fromPanel)
            else:
                return self._findBottommostPanel(right, fromPanel)

        return candidate

    def _findLeftNeighbor(self, panel : Panel):
        parent =  panel.getParent()
        if parent is None:
            # Root panel has no neighbors
            return None

        leftCandidate = parent.getLeft()
        if parent.getRight() == panel and leftCandidate is not None:
            return self._findRightmostPanel(leftCandidate, panel)
        else:
            return self._findLeftNeighbor(parent)

    def _findRightNeighbor(self, panel : Panel):
        """ Walks upward until it finds a parent in which this panel is on the
        left of a vertical split. """
        parent = panel.getParent()
        if parent is None:
            # Root panel has no neighbors
            return None

        rightCandidate = parent.getRight()
        if parent.getLeft() == panel and rightCandidate is not None:
            return self._findLeftmostPanel(rightCandidate, panel)
        else:
            return self._findRightNeighbor(parent)

    def _findTopNeighbor(self, panel : Panel):
        parent = panel.getParent()
        if parent is None:
            return None

        topCandidate = parent.getTop()
        if parent.getBottom() == panel and topCandidate is not None:
            return self._findTopmostPanel(topCandidate, panel)
        else:
            return self._findBottomNeighbor(parent)

    def _findBottomNeighbor(self, panel : Panel):
        parent = panel.getParent()
        if parent is None:
            return None

        bottomCandidate = parent.getBottom()
        if parent.getTop() == panel and bottomCandidate is not None:
            return self._findBottommostPanel(bottomCandidate, panel)
        else:
            return self._findTopNeighbor(parent)

    def traversePanelLeft(self):
        neighbor = self._findLeftNeighbor(self._selectedPanel)
        if neighbor is not None:
            self.selectPanel(neighbor)

    def traversePanelRight(self):
        """ Traverses the current selected panel to the panel diretly right 
        of the current selected panel, if one exsts """
        neighbor = self._findRightNeighbor(self._selectedPanel)
        if neighbor is not None:
            self.selectPanel(neighbor)

    def traversePanelUp(self):
        neighbor = self._findTopNeighbor(self._selectedPanel)
        if neighbor is not None:
            self.selectPanel(neighbor)
    
    def traversePanelDown(self):
        neighbor = self._findBottomNeighbor(self._selectedPanel)
        if neighbor is not None:
            self.selectPanel(neighbor)

    def mainLoop(self):
        """Continually update menus and elements until the program exits"""
        while self.shouldExit == False:
            if self._selectedPanel is None or not self._selectedPanel.hasMenu():
                self.selectPanel(self._rootPanel)

            self.update()
            self.display()
            key = self.stdscr.getch()
            if key == -1:
                # Continue on timeout character
                continue
            elif key == curses.KEY_RESIZE:
                # Update window size when window is resized
                self.updateWindowSize()
                self.update()
            elif key == 3: 
                # Exit on Ctrl+C
                self.shouldExit = True
            elif key in KEYBINDS['panelDown']: # Capital J or Shift+up arrow
                # Move down a panel
                self.traversePanelDown()
            elif key in KEYBINDS['panelRight']: # ctrl+L or shift+right arrow
                # Move right a panel
                self.traversePanelRight()
            elif key in KEYBINDS['panelUp']: # ctrl+K or shift+down arrow
                # Move up a panel
                self.traversePanelUp()
            elif key in KEYBINDS['panelLeft']: # Ctrl + L or shift+left
                # Move left a panel
                self.traversePanelLeft()
            else:
                # Pass other inputs to current menu
                if self._selectedPanel is not None:
                    menu = self._selectedPanel.getMenu()
                    if menu is not None:
                        menu.handleInput(key)

    def splitHorizontal(self):
        """ Split the root panel horizontally. This method can only be called once, and
        can only be called if the panel is not already split vertically.
        :returns: The left and right panels that are split
        :rtype: tuple[Panel, Panel]
        """
        return self._rootPanel.splitHorizontal()

    def splitVertical(self):
        """Split the root panel horizontally. This method can only be called once, and 
        can only be called if the root panel is not already split horizontally.
        :returns: The top and bottom panels that are split
        :rtype: tuple[Panel, Panel]
        """
        return self._rootPanel.splitVertical()

    def addMenu(self, menu : Menu):
        """ Add a menu to the manager's dictionary of menus"""
        self._menus[menu.name] = menu

    def getMenuByName(self, name : str):
        """ Get a menu from the dict of menus with given name """
        if name not in self._menus.keys():
            raise Exception(f"Menu with name, {name}, does not exist in manager")
        
        return self._menus[name]
