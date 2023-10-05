from typing import Callable
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


class ViewModelMeta(type(QObject)):
    """
    Metaclass for view models
    """
    def __new__(cls, name, bases, attrs):
        view_model_fields = [
            attr_value
            for attr_value in attrs.values()
            if isinstance(attr_value, ViewModelField)
        ]
        return super().__new__(cls, name, bases, attrs)


class PSViewModel(QObject, metaclass=ViewModelMeta):
    """
    Base class for view models
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




