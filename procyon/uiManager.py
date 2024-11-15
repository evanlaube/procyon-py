import curses
import time

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

        self.updateWindowSize()

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
        """ Displays the current state of the menu """
        if self.currentMenu is not None:
           self.stdscr.clear()
           self.menus[self.currentMenu].update()
           self.menus[self.currentMenu].display(self.stdscr)

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

