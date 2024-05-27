from typing import Callable
from contextlib import contextmanager

from PySide6.QtCore import QObject, Signal


class ViewModelField:
    """
    Descriptor for view model fields
    """
    def __set_name__(self, owner, name):
        """
        Sets a name for the `PSViewModel`, which can be accessed through public
        and private attributes, and has methods to signal updates and retrieve the
        last update time.

        Args:
            owner (`PSViewModel`.): view model object that will receive the newly
                created field.
                
                		- `isSubclass(owner, PSViewModel)` - This is used to check if
                `owner` is a subclass of `PSViewModel`. If it's not, a `TypeError`
                is raised.
                		- `self.__public_name` - This attribute holds the name of the
                view model.
                		- `self.__private_name` - This attribute holds a privately
                accessible name for the view model.
                		- `self.__awaits_update_name` - This attribute holds a name for
                the awaiter of updates to the view model.
                		- `self.__was_updated_name` - This attribute holds a name for
                the previous value of the view model.
                		- `self.__updated_signal_name` - This attribute holds the name
                of the signal emitted when the view model is updated.
            name (str): public name of the view model field.

        """
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
        """
        Sets an instance attribute `self.__private_name`. If it hadn't been updated
        before, emits the update signal and sets a flag `self.__was_updated_name`.

        Args:
            instance (object.): Python object to which the method is being applied.
                
                	1/ `self.__private_name`: The name of a private attribute that
                holds the updated value of the instance.
                	2/ `self.__awaits_update_name`: An instance attribute that indicates
                whether the object's `__updated_signal_name` should be emitted
                after setting the value.
                	3/ `self.__updated_signal_name`: The name of a signal emitted
                when the object's value has been updated.
                	4/ `self.__was_updated_name`: An instance attribute that indicates
                whether the object's `__updated_signal_name` has been emitted previously.
            value (object.): value that is being assigned to the private attribute
                of an instance.
                
                	1/ `instance`: This is the object instance that is being updated.
                	2/ `self`: This refers to the class or object that the `__set__`
                method is a part of.
                	3/ `self.__private_name`: This is the name of a private attribute
                in the class that is being updated.
                	4/ `value`: This is the value that is being assigned to the private
                attribute `self.__private_name`.
                	5/ `getattr()`: This is a function that retrieves an attribute
                from an object. In this case, it retrieves the value of the private
                attribute `self.__awaits_update_name`.
                	6/ `setattr()`: This is a function that sets an attribute on an
                object. In this case, it sets the value of the private attribute
                `self.__was_updated_name` to `True`.
                	7/ `self.__updated_signal_name`: This is the name of a signal in
                the class that is emitted when the private attribute
                `self.__awaits_update_name` is changed.

        """
        setattr(instance, self.__private_name, value)
        if not getattr(instance, self.__awaits_update_name):
            getattr(instance, self.__updated_signal_name).emit()
        else:
            setattr(instance, self.__was_updated_name, True)


class PSViewModel(QObject):
    """
    Base class for view models
    """
    updated = Signal()
    error = Signal(Exception)

    def __init__(self):
        """
        Sets the `__awaits_update` and `__was_updated` instance variables to `False`.

        """
        super().__init__()
        self.__awaits_update = False
        self.__was_updated = False

    @contextmanager
    def update(self, silent: bool = False):
        """
        Updates the object's properties based on its own attributes and external
        factors, then emits an "updated" signal if applicable and possible.

        Args:
            silent (False): ability to suppress emission of the `updated` signal
                when the function successfully updates the object's state without
                any errors, which means that it prevents the `updated` signal from
                being emitted unnecessarily.

        """
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




