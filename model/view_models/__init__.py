"""
View models module
Contains the base class for view models
The main idea of data flow is that on ViewModel update, service updates
db model and then generates new view item - to not create circular updates

Classes:
    ViewModelField: Descriptor for view model fields
    PSViewModel: Base class for view models
Submodules:
    link - view model for id-name pair entities
    song - view model for song entity
"""
from contextlib import contextmanager

from PySide6.QtCore import QObject, Signal


class ViewModelField:
    """
    Descriptor for view model fields
    """
    def __set_name__(self, owner, name):
        if not issubclass(owner, PSViewModel):
            raise TypeError("ViewModelField must be used only with view models")
        self.__public_name = name
        self.__private_name = f"_{owner.__name__}__{name}"
        self.__awaits_update_name = f"_PSViewModel__awaits_update"
        self.__was_updated_name = f"_PSViewModel__was_updated"
        self.__updated_signal_name = "updated"

    def __get__(self, instance, owner):
        return getattr(instance, self.__private_name)

    def __set__(self, instance, value):
        setattr(instance, self.__private_name, value)
        if not getattr(instance, self.__awaits_update_name):
            getattr(instance, self.__updated_signal_name).emit()
        else:
            setattr(instance, self.__was_updated_name, True)


class PSViewModel(QObject):
    """
    Base class for view models:

    Signals:
        updated: emitted when the view model was updated
        error: emitted when an error occurred during the update

    Methods:
        update: context manager that allows to emit updated signal
            on the exit from the context and only if the view model was updated.
            That is useful to update many fields at once and emit the signal only once.
            Also, it allows to pass silent=True to suppress the signal emission at all.
    """
    updated = Signal()
    error = Signal(Exception)

    def __init__(self):
        super().__init__()
        self.__awaits_update = False
        self.__was_updated = False

    @contextmanager
    def update(self, silent: bool = False):
        try:
            self.__was_updated = False
            self.__awaits_update = True
            yield self
        except Exception as e:
            self.error.emit(e)
        finally:
            self.__awaits_update = False
            if self.__was_updated and not silent:
                self.updated.emit()




