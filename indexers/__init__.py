from abc import ABC, abstractmethod
from typing import Any, TypeVar, Generic, Hashable, Optional
from weakref import WeakValueDictionary

SourceType = TypeVar("SourceType")
ResultType = TypeVar("ResultType")
KeyType = TypeVar("KeyType", bound=Hashable)
Default = TypeVar("Default")


class AbstractIndexer(ABC, Generic[KeyType, SourceType, ResultType]):
    """
    Abstract Generic Indexer object. Have already implemented dictionary-like behaviour:
    allows to get item by id, has get method. To ensure ids integrity inserting at key
    is not allowed, add method implemented instead

    Indexer ensures that in its context instance with the same id will exist only in singular.
    It should implement some mapping between a class that serves as data source and a class
    which models are stored in index. Also, it should implement a mapping between a data
    source class instance and some hashable type that will serve as id.

    To set correct type checking You need to provide
        KeyType - Hashable type that represents identifier, which is
            used as keys in the index
        SourceType - type of the object that is used as data source
            to create and update values in the index
        ResultType - type of the object values that are present in index

    Should implement methods:
        obtain_id - function that when given a data source object will return
            an id for it
        create_object - function that when given a data source object will
            return corresponding value to be stored in the index
        update_object - function that when given a data source object and
            value from the index will update value from index to represent
            that data source object
    implemented methods:
        exists - checks if there is an object in the index that corresponds to provided
            data source one
        get - dictionary-like method that returns an object by id or default if there is no such object
        add - adds an object to the index
    """
    def __init__(self):
        self.__index = WeakValueDictionary()

    @abstractmethod
    def obtain_id(self, obj: SourceType) -> KeyType: ...

    @abstractmethod
    def create_object(self, obj: SourceType) -> ResultType: ...

    @abstractmethod
    def update_object(self, old_obj: ResultType, new_obj: SourceType) -> None:
        ...

    def exists(self, obj: SourceType) -> bool:
        return self.obtain_id(obj) in self.__index

    def __getitem__(self, item: KeyType) -> ResultType:
        return self.__index[item]

    def get(self, item: KeyType, default: Optional[Default] = None) -> ResultType | Default | None:
        return self.__index.get(item, default)

    def add(self, item: SourceType) -> ResultType:
        if self.exists(item):
            result = self[self.obtain_id(item)]
            self.update_object(result, item)
        else:
            result = self.create_object(item)
            self.__index[self.obtain_id(item)] = result
        return result
