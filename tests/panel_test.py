

import curses
from procyon.button import Button
from procyon.label import Label
from procyon.menu import Menu
from procyon.uiManager import UIManager

def buttonFunction():
    return "Clicked!"

def main(stdscr: curses.window):
    manager = UIManager(stdscr)
    mainMenu = Menu('main') 
    manager.addMenu(mainMenu)
    manager.switchMenu('main')

    for i in range(10):
        buttonLabel = f"Button {i}"
        button = Button(buttonLabel, buttonFunction)
        button.setLabelToResult = True
        mainMenu.addElement(str(i), button)

    top, bottom = manager._rootPanel.splitHorizontal()
    topLeft, topRight = top.splitVertical()

    bottom.loadMenu(mainMenu)

    manager.run()


if __name__ == '__main__':
    curses.wrapper(main)
    
