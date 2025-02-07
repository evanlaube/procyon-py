

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
    manager.addMenu(mainMenu)

    topLeftMenu = Menu('tl')
    topLeftMenu.setDesiredSize(30, 8)
    for i in range(10):
        buttonLabel = f"TLButton {i}"
        button = Button(buttonLabel, buttonFunction)
        button.setLabelToResult = True
        topLeftMenu.addElement(str(i), button)
    topLeftMenu.elements['1'].setMaxWidth(10)
    manager.addMenu(topLeftMenu)
    
    topRightMenu = Menu('tr')
    topRightMenu.setDesiredSize(30, 8)
    for i in range(10):
        buttonLabel = f"TRButton {i}"
        button = Button(buttonLabel, buttonFunction)
        button.setLabelToResult = True
        topRightMenu.addElement(str(i), button)
    manager.addMenu(topRightMenu)

    top, bottom = manager.splitHorizontal()
    top.setSize(-1, 8)
    topLeft, topRight = top.splitVertical()
    tll, tlr = topLeft.splitVertical()


    bottom.loadMenu(manager.getMenuByName('main'))
    tll.loadMenu(manager.getMenuByName('tl'))
    tlr.loadMenu(manager.getMenuByName('main'))
    topRight.loadMenu(manager.getMenuByName('tr'))

    manager.run()


if __name__ == '__main__':
    curses.wrapper(main)
    
