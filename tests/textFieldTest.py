
import curses

from procyon import UIManager, Menu, Panel, TextField

def main(stdscr: curses.window):
    manager = UIManager(stdscr)
    mainMenu = Menu("main")

    textField1 = TextField("Text1")
    textField1.setMaxWidth(60)
    textField2 = TextField("Text2")
    textField3 = TextField("Text3")
    textField4 = TextField("Text4")
    mainMenu.addElement('textField1', textField1)
    mainMenu.addElement('textField2', textField2)
    mainMenu.addElement('textField3', textField3)
    mainMenu.addElement('textField4', textField4)

    manager._rootPanel.loadMenu(mainMenu)

    manager.run()

if __name__ == '__main__':
    curses.wrapper(main)
