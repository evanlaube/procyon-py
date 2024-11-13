import curses
import time

class UIManager:
    """A class for managing and running all UI functions. The UIManager stores a dict of
    menus to easily switch between them, and passes keyboard inputs to the selected menu only,
    as well as updating the menu
    :param stdscr: The screen to print menus to
    """
    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.currentMenu = None
        self.menus = {} 
        self.shouldExit = False

        curses.curs_set(0)
        curses.start_color()
        curses.use_default_colors()

        # Background color pallette (XTerm-256)
        bgColors = [-1,0,1,2,3,4,5,6,236]

        for i in range(len(bgColors)):
            for n in range(16):
                curses.init_pair(i*16+n, n-1, bgColors[i])


        # Initialize color pairs
        #for i in range(1, min(curses.COLORS-2, 128+16)):
        #    curses.init_pair(i,(i%16)-1, bgColors[(i//16)-1])
        #try:
        #    curses.init_pair(0, -1, -1)
        #except:
        #    # TODO: Fix windows color schemes
        #    pass

        self.stdscr.bkgd(' ', curses.color_pair(0))
        self.stdscr.clear()
        self.stdscr.refresh()
        self.stdscr.timeout(100)

    def run(self):
        """Reset the current display and run the main loop"""
        self.stdscr.clear()
        self.stdscr.refresh()
        self.mainLoop()

    def mainLoop(self):
        """Continually update menus and elements until the program exits"""
        try:
            while self.shouldExit == False:
                if self.currentMenu != None:
                    self.stdscr.clear()
                    self.menus[self.currentMenu].update()
                    self.menus[self.currentMenu].display(self.stdscr)
                key = self.stdscr.getch()
                self.menus[self.currentMenu].handleInput(key)
        except KeyboardInterrupt:
            self.shouldExit = False 

    def addMenu(self, menu):
        """Insert a menu into the dictionary of menus. Note that menus can
        be overwritten without warning.
        :param menu: The menu to insert
        :type menu: ui.Menu
        """
        name = menu.name

        self.menus[name] = menu

    def switchMenu(self, menu):
        """Switch the currently displayed menu
        :param menu: The name of the menu to switch to
        :type menu: str
        """
        if menu in self.menus.keys():
            self.currentMenu = menu

