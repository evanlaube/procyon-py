
from .element import Element
from .container import Container 

class RowBar(Container):
    """An element container for displaying multiple elements inline in a menu.
    :param elements: A list of Elements that will be added to the RowBar
    :type elements: list
    :param separator: The character(s) that will be printed between each element in the bar
    :type separator: str, optional
    """
    def __init__(self, elements : list[Element], separator : str = '\t', color : int = 0,):
        """Constructor method
        """
        super().__init__(elements, separator, color)








