
import curses

from procyon import UIManager, Menu, Panel, TextField

def main(stdscr: curses.window):
    manager = UIManager(stdscr)
    mainMenu = Menu("main")

    textField = TextField("Text")
    mainMenu.addElement('textField', textField)

    manager._rootPanel.loadMenu(mainMenu)

    manager.run()

if __name__ == '__main__':
    curses.wrapper(main)
