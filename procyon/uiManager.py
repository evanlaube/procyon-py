import curses
from re import L
import time

from procyon.panel import Panel

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
        self.currentMenu = None
        self.menus = {} 
        self.shouldExit = False

        self._rootPanel = Panel()
        self.updateWindowSize()

        # Create a root panel to contain all other panels
        # Make root panel fill window
        self._rootPanel.setSize(self.cols, self.rows)

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

        for i in range(len(bgColors)):
            for n in range(16):
                curses.init_pair(i*16+n, n-1, bgColors[i])

    def updateWindowSize(self):
        ''' Gets the current size of the curses window and stores it in member
        variables self.rows and self.cols'''
        self.rows, self.cols = self.stdscr.getmaxyx()
        # Subtract one from cols to prevent error when printing in bottom right corner
        self.cols -= 1

        self._updatePanelSize(self._rootPanel, self.rows, self.cols)

    def _updatePanelSize(self, panel : Panel, rows : int, cols : int):
        panel.setSize(cols, rows)

        left = panel.getLeft()
        right = panel.getRight()
        top = panel.getTop()
        bottom = panel.getBottom()

        if left is not None and right is not None:
            leftCols = cols // 2 
            rightCols = cols = leftCols

            self._updatePanelSize(left, rows, leftCols)
            self._updatePanelSize(right, rows, rightCols)
        elif top is not None and bottom is not None:
            topRows = rows // 2
            bottomRows = rows - topRows
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
        if self.currentMenu is not None:
           self.stdscr.clear()
           #self.menus[self.currentMenu].update()
           #self.menus[self.currentMenu].display(self.stdscr)
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
                self._recDisplayPanel(panel.getRight(), (position[0]+leftSize[0], position[1]))
                
                try:
                    for y in range(position[1], position[1] + leftSize[1] + 1): # TODO: Figure out this +1
                        self.stdscr.addstr(y, position[0]+leftSize[0], verticalSep) 
                except:
                    return
        else:
            # Update Menu
            menu.update()

            # TODO: Figure out how to determine if panel is selceted
            panelSelected = True

            # Display Menu
            elements = menu.elements 
            startY = position[1]
            startX = position[0]
            for id, key in enumerate(elements.keys()):
                element = elements[key]
                selected = panelSelected & (id == menu.selectedIndex)

                y = startY + id
                if y > startY + panel.getSize()[1]-1:
                    break
                elementStr = element.getStr(selected) 
                for x in range(len(elementStr)):
                    if x + startX > panel.getSize()[0]-1:
                        break
                    char = elementStr[x]
                    try:
                        self.stdscr.addstr(y+1, x+startX, char)
                    except:
                        continue

    def mainLoop(self):
        """Continually update menus and elements until the program exits"""
        try:
            while self.shouldExit == False:
                self.display()
                key = self.stdscr.getch()
                if key == -1:
                    # Continue on timeout character
                    continue
                elif key == curses.KEY_RESIZE:
                    # Update window size when window is resized
                    self.updateWindowSize()
                    self.menus[self.currentMenu].update()
                elif key == 3: 
                    # Exit on Ctrl+C
                    self.shouldExit = True
                else:
                    # Pass other inputs to current menu
                    self.menus[self.currentMenu].handleInput(key)
        except KeyboardInterrupt:
            self.shouldExit = True 

    def addMenu(self, menu : Menu):
        """Insert a menu into the dictionary of menus. Note that menus can
        be overwritten without warning.
        :param menu: The menu to insert
        :type menu: ui.Menu
        """
        name = menu.name
        self.menus[name] = menu

    def switchMenu(self, menuName : str):
        """Switch the currently displayed menu
        :param menu: The name of the menu to switch to
        :type menu: str
        """
        if menuName in self.menus.keys():
            self.currentMenu = menuName 

