

import curses
from procyon import Button
from procyon.label import Label
from procyon.menu import Menu
from procyon.uiManager import UIManager

def buttonFunction():
    return "Clicked!"

def main(stdscr: curses.window):
    manager = UIManager(stdscr)

    left, right = manager.splitVertical()
    
    leftMenu = Menu('leftMenu')
    rightMenu = Menu('rightMenu')

    leftTitle = Label("Left Menu".center(30, '-'))
    rightTitle = Label("Right Menu".center(30, '-'))

    leftMenu.addElement('title', leftTitle)
    rightMenu.addElement('title', rightTitle)

    for i in range(200):
        num = str(i)
        leftButton = Button('leftButton' + num, buttonFunction, setLabelToResult=True)
        rightButton = Button('rightButton' + num,  buttonFunction, setLabelToResult=True)

        leftMenu.addElement('button'+num, leftButton)
        rightMenu.addElement('button'+num, rightButton)

    left.loadMenu(leftMenu)
    right.loadMenu(rightMenu)

    manager.run()


if __name__ == '__main__':
    curses.wrapper(main)
    
