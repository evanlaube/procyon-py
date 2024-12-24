
import curses
from procyon.checkBox import CheckBox
from procyon.label import Label
from procyon.menu import Menu
from procyon.button import Button
from procyon.rowBar import RowBar
from procyon.uiManager import UIManager

def buttonFunction():
    return str('clicked')

def main(stdscr: curses.window):
    # Clear screen
    stdscr.clear()

    manager = UIManager(stdscr)

    mainMenu = Menu('main')

    mainMenu.addElement("title", Label("Interactive test:\nSecond line of label"))

    rowBarLabels = ['rowBarButton1', 'rowBarButton2', 'rowBarButton3']
    elements = []
    for label in rowBarLabels:
        button = Button(label, lambda: buttonFunction())
        button.setLabelToResult = True
        elements.append(button)
    bar = RowBar(elements, '\t')
    mainMenu.addElement("buttonRowbar", bar)

    buttonLabels = ['Button1', 'Button2', 'Button3']
    for label in buttonLabels:
        button = Button(label, lambda: buttonFunction())
        button.setLabelToResult = True
        mainMenu.addElement(label, button)

    checkboxLabels = ['Checkbox 1', 'Checkbox 2', 'Checkbox 3']
    for label in checkboxLabels:
        checkbox = CheckBox(label)
        mainMenu.addElement(label, checkbox)

    sizeLabel = Label('Size', refreshFunction=lambda m=manager: f'{m.rows}, {m.cols}')
    mainMenu.addElement('sizeLabel', sizeLabel) 

    manager._rootPanel.loadMenu(mainMenu)

    manager.run()
    

if __name__ == "__main__":
    curses.wrapper(main)
