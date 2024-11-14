
import curses
from procyon.label import Label
from procyon.menu import Menu
from procyon.button import Button
from procyon.rowBar import RowBar
from procyon.uiManager import UIManager

def buttonFunction():
    return "Clicked!" 

def main(stdscr: curses.window):
    # Clear screen
    stdscr.clear()

    manager = UIManager(stdscr)

    mainMenu = Menu('main')

    mainMenu.addElement("title", Label("Interactive test:"))

    rowBarLabels = ['rowBarButton1', 'rowBarButton2', 'rowBarButton3']
    elements = []
    for label in rowBarLabels:
        button = Button(label, lambda: buttonFunction)
        elements.append(button)
    bar = RowBar(elements, '\t')
    mainMenu.addElement("buttonRowbar", bar)

    buttonLabels = ['Button1', 'Button2', 'Button3']
    for label in buttonLabels:
        button = Button(label, lambda: buttonFunction)
        mainMenu.addElement(label, button)


    manager.addMenu(mainMenu)
    manager.switchMenu('main')
    manager.run()
    

if __name__ == "__main__":
    curses.wrapper(main)
