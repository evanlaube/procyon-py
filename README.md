# procyon-py
Procyon is a lightweight terminal UI library for python that simplifies building rich, interactive 
interfaces directly in the terminal. It allows users to split windows into multiple 
panels and populate them with various UI elements for a fully customizable experience.

## Features
- **Panel Splitting**: Divide your terminal into several different panels - each with its own menu
- **Flexible Layouts**: Add elements and containers to menus in a line by line approach
- **Elements**: Support for buttons, checkboxes, progress bars, labels, and many more types of elements
- **Scalability**: Panels support resizing dynamically when resizing the terminal
- **Straightforward approach**: A simple menu building system allows for quick development

## Installation

#### Prerequisites
- Python 3.7 or higher
- `curses` library

#### Create a Virtual Environment (Optional but recommended)
This step can be safely skipped if you are already using a default virtual Environment.
```bash
python -m venv venv
source venv/bin/activate # On Windows use: venv\Scripts\activate
```

#### Windows Only
As of now, on windows, in order for procyon to work, the `windows-curses` package must be installed with
```bash
pip install windows-curses
```

#### Install Procyon
```bash
pip install procyon-py
```

## Quick Start Example
This code is an example that creates two simple menus split vertically with some elements
included.

```python
import curses
from procyon import UIManager, Menu, Panel, Button, Label

def buttonFunction():
    ''' Runs when the button is activated '''
    return "Clicked!"

def main(stdscr: curses.window):
    # Initialize a ui manager with the curses window
    manager = UIManager(stdscr)

    # Create a menu for the left panel and insert elements
    leftMenu = Menu('left')
    leftLabel = Label("Left menu")
    leftButton1 = Button("Button1", buttonFunction, setLabelToResult=True)
    leftButton2 = Button("Button2", buttonFunction, setLabelToResult=True)
    leftMenu.addElement(leftLabel)
    leftMenu.addElement(leftButton1)
    leftMenu.addElement(leftButton2)

    # Create a menu for the right panel and insert elements
    rightMenu = Menu('right')
    rightLabel = Label("Right menu")
    rightButton = Button("Click me!", buttonFunction, setLabelToResult=True)
    rightMenu.addElement(rightLabel)
    rightMenu.addElement(rightButton)

    # Split the uiManager root panel in two
    left, right = manager.splitVertical()

    # Load menus into left and right panels
    left.loadMenu(leftMenu)
    right.loadMenu(rightMenu)

    # Run the uiManager
    manager.run()

if __name__ == "__main__":
    # Pass the curses window to the main function
    curses.wrapper(main)
```

## Element types
Procyon has support for many different types of elements, and many more are planned!

#### Currently implemented element types
- **Label**: A simple line of text that can be easily updated
- **Button**: Activate with enter to run a function. 
- **Checkbox**: Toggle state with enter. 
- **Progress Bar**: Visually show a percentage (Ex. Time played of song on a music player)
- **Row bar**: A horizontal container to display multiple elements inline

## Usage
#### Menus
In procyon, a menu is a container for a list of elements. When adding elements to a menu,
an element is specified, along with an id string for the element. This id string can be
used to easily access elements to modify them. A menu must be loaded into a panel to be displayed

#### Panels
A panel is a method for splitting up the window that Procyon is running in. A panel can either
contain a menu, or two separate panels. Each panel can be split into only two panels, either
vertically or horizontally. If a panel contains a menu, that menu will be drawn inside of 
it when the manager is displayed.

#### UIManager
The UIManager is the heart of the UI. It handles displaying and updating panels and their menus,
as well as capturing user input. The UIManager also keeps track of which panel is selected, which
can be changed by the user using keyboard controls. The UIManager runs a main loop that refreshes
every time the user makes an input, or every 100 milliseconds. 

## Controls
Procyon is controlled entirely by the keyboard - there is no mouse support (yet...).
Users can use either the arrow keys or vim style directional keys (h,j,k,l). UI Elements 
can be 'clicked' or activated using the enter/return key

#### Switching panels
As of now, panels are switched using shift + a directional key. For example, to move to the
panel on top of the current panel, `shift + up arrow` or `shift + K` can be used

## Contributing
Contributions to Procyon are not only welcome, but highly encouraged!
For more details on how to contribute, visit the [CONTRIBUTING](CONTRIBUTING.md) guidelines

## Get involved
If you have and questions, suggestions, or feedback, please don't hesitate to 
[open an issue](https://github.com/evanlaube/procyon-py/issues) or [contact me](mailto:laubeevan@gmail.com).
