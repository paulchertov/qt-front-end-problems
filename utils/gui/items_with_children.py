"""
Module contains helper functions to work with children items
functions:
    clear_items - empties layout, removing widget one after another
        also marks widgets to be deleted
"""

from PySide6.QtWidgets import QLayout


def clear_items(layout: QLayout):
    """
    Removes widgets from a `QWidgetLayout` instance by iterating over its items,
    removing each item's widget and deleting it once removed.

    Args:
        layout (QLayout): 2D layout of the widgets in the main widget, and it is
            used to remove widgets from the layout by taking them at the index 0
            when their count is greater than 0.

    """
    while layout.count() > 0:
        item = layout.takeAt(0)
        widget = item.widget()
        if widget:
            layout.removeWidget(widget)
            widget.deleteLater()

