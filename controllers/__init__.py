"""
Module contains resources common to all or many
controllers
classes:
    PSWithViewMixin - controller with view mixin unifies gui installation
"""

import os
from typing import Optional, Callable, List, ClassVar

from PySide6.QtUiTools import QUiLoader


class PSWithViewMixin:
    """
    A mixin class that provides common functionality for GUI controllers.
    class methods:
        set_qui_files_folder: sets folder path for all classes or subclasses
            of particular class.
    class fields:
        qss_text: cached contents of the .qss file as a string.
        gui_name: The name of the .ui and .qss files. Should be overridden in
            children.
    fields:
        gui_name_template: A template for the gui_name variable
    properties:
        gui_path: path to the .ui file. May be overridden in children if needed.
        qss_path: path to the .qss file. May be overridden in children if needed.
        qt_loader: A reusable QUiLoader object for all instances of the class.
            Read only.
    methods:
        install_gui: load the .ui file to create a Qt widget in the view attribute.
        set_styles: apply styles to the view from the .qss file.
        view_handler: add controller's handler method to the controller's view.
        view_handlers: apply the previous method to a list of handlers
    """
    # create one reusable loader for all instances
    __qt_loader: QUiLoader = QUiLoader()

    # styles text (will be saved in class variable for not reopening .qss file)
    qss_text: ClassVar[str] = ""

    # gui_name class variable should be defined in main class
    # gui_name.qss and gui_name.ui files from which styles and ui to be loaded
    gui_name: ClassVar[str] = ""

    # gui_name_template serves
    gui_name_template: ClassVar[str] = "gui"

    @classmethod
    def set_gui_files_folder(cls, folder_path: str, globally: Optional[bool] = True):
        """
        Set the folder path for the UI and QSS files.
        If `globally` is set to True, the value is set for the
        `PSWithViewMixin` class, otherwise the value is set for the current
        class
        :param str folder_path: the folder path for the UI and QSS files
        :param Optional[bool] globally: whether to set the value globally for
            `PSWithViewMixin` class or only for the current class.
            Defaults to True.
        :return: None
        """
        klass = PSWithViewMixin if globally else cls
        klass.gui_name_template = folder_path

    @property
    def gui_path(self) -> str:
        if not self.gui_name:
            raise AttributeError(f"Gui name was not set on class {self.__class__.__name__}")
        return os.path.join(
            self.gui_name_template, f'{self.gui_name}.ui'
        )
    
    @property
    def qss_path(self) -> str:
        if not self.gui_name:
            raise AttributeError(f"Gui name was not set on class {self.__class__.__name__}")
        return os.path.join(
            self.gui_name_template, f'{self.gui_name}.qss'
        )
        
    @property
    def qt_loader(self) -> QUiLoader:
        return self.__qt_loader
    
    def install_gui(self):
        """
        Create widget from corresponding .ui file into self.view
        :return: None
        """
        self.view = self.qt_loader.load(self.gui_path)

    def set_styles(self, reload: bool = False) -> None:
        """
        Applies styles to controller's widget, loads styles from corresponding
        .qss file. Uses cached value if reload was not set to True
        :param bool reload: reload styles from file or just set from class var
        :return: None
        """
        if not self.qss_text or reload:

            style_path = os.path.abspath(self.qss_path)
            try:
                with open(style_path, 'r') as file:
                    self.__class__.qss_text = file.read()
            except FileNotFoundError as e:
                pass
        self.view.setStyleSheet(self.qss_text)

    def view_handler(self, handler: Callable):
        """
        If controller is not QWidget, all handlers could be added
        to its view to work as intended. This method does
        self.view.method = self.method for provided method
        :param Callable handler: handler method
        :return: None
        """
        setattr(self.view, handler.__name__, handler)

    def view_handlers(self, handlers: List[Callable]):
        """
        WithViewMixin.view_handler for list of handlers
        :param List[Callable] handlers: list of qt events handlers
        :return: None
        """
        for handler in handlers:
            self.view_handler(handler)
