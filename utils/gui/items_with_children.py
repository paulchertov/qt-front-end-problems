"""
Module contains helper functions to work with children items
functions:
    clear_items - empties layout, removing widget one after another
        also marks widgets to be deleted
"""

from PySide6.QtWidgets import QLayout


def clear_items(layout: QLayout):
    """
    Clears all widgets from layout
    :param layout: layout to clear
    :return: None
    """
    while layout.count() > 0:
        item = layout.takeAt(0)
        widget = item.widget()
        if widget:
            layout.removeWidget(widget)
            widget.deleteLater()

