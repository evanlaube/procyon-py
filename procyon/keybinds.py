
import platform

SYSTEM = platform.system()


if SYSTEM == 'Linux':
    KEYBINDS = {
        'enter': [10],
        'backspace': [263],
        'backspaceWord': [8],
        'panelLeft': [72, 393],    # Shift + H or Shift + leftArrow
        'panelDown': [74, 336],   # Shift + J or Shift + downArrow
        'panelUp': [75, 337],     # Shift + K or Shift + upArrow
        'panelRight': [76, 402],  # Ctry + L or Shift + leftArrow
        'moveLeft': [ 260, 104],  # H or leftArrow
        'moveDown': [258, 106],   # J or downArrow
        'moveUp': [259, 107],     # K or upArrow
        'moveRight': [261, 108],  # L or rightArrow
    }
elif SYSTEM == "Darwin":
    KEYBINDS = {
        'enter': [10],
        'backspace': [127],
        'backspaceWord': [8],
        'panelLeft': [72, 393],    # Shift + H or Shift + leftArrow
        'panelDown': [74, 336],   # Shift + J or Shift + downArrow
        'panelUp': [75, 337],     # Shift + K or Shift + upArrow
        'panelRight': [76, 402],  # Ctry + L or Shift + leftArrow
        'moveLeft': [ 260, 104],  # H or leftArrow
        'moveDown': [258, 106],   # J or downArrow
        'moveUp': [259, 107],     # K or upArrow
        'moveRight': [261, 108],  # L or rightArrow
    }
else:
    # Just set to Mac keybinds by default. TODO: Add support for Windows
    KEYBINDS = {
        'enter': [10],
        'backspace': [127],
        'backspaceWord': [8],
        'panelLeft': [72, 393],    # Shift + H or Shift + leftArrow
        'panelDown': [74, 336],   # Shift + J or Shift + downArrow
        'panelUp': [75, 337],     # Shift + K or Shift + upArrow
        'panelRight': [76, 402],  # Ctry + L or Shift + leftArrow
        'moveLeft': [ 260, 104],  # H or leftArrow
        'moveDown': [258, 106],   # J or downArrow
        'moveUp': [259, 107],     # K or upArrow
        'moveRight': [261, 108],  # L or rightArrow
    }

