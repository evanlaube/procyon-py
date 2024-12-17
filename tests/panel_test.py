

import curses
from procyon import Button
from procyon.label import Label
from procyon.menu import Menu
from procyon.uiManager import UIManager

def buttonFunction():
    return "Clicked!"

def main(stdscr: curses.window):
    manager = UIManager(stdscr)

    mainMenu = Menu('main') 
    for i in range(10):
        buttonLabel = f"Button {i}"
        button = Button(buttonLabel, buttonFunction)
        button.setLabelToResult = True
        mainMenu.addElement(str(i), button)

    topLeftMenu = Menu('tl')
    topLeftMenu.setDesiredSize(30, -1)
    for i in range(10):
        buttonLabel = f"TLButton {i}"
        button = Button(buttonLabel, buttonFunction)
        button.setLabelToResult = True
        topLeftMenu.addElement(str(i), button)
    topLeftMenu.elements['1'].setMaxWidth(10)
    
    topRightMenu = Menu('tr')
    for i in range(10):
        buttonLabel = f"TRButton {i}"
        button = Button(buttonLabel, buttonFunction)
        button.setLabelToResult = True
        topRightMenu.addElement(str(i), button)

    top, bottom = manager.splitHorizontal()
    topLeft, topRight = top.splitVertical()

    bottom.loadMenu(mainMenu)
    topLeft.loadMenu(topLeftMenu)
    topRight.loadMenu(topRightMenu)

    manager.run()


if __name__ == '__main__':
    curses.wrapper(main)
    
