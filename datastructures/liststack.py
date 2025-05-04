from datastructures.istack import IStack
from datastructures.linkedlist import LinkedList
from typing import Generic, TypeVar

T = TypeVar('T')

class ListStack(Generic[T], IStack[T]):
    def __init__(self, data_type: object) -> None:
        self._data_type = data_type
        self._list = LinkedList[T]()

    def push(self, item: T):
        if not isinstance(item, self._data_type):
            raise TypeError(f"Expected item of type {self._data_type}, got {type(item)}.")
        self._list.prepend(item)

    def pop(self) -> T:
        if self.empty:
            raise IndexError("Pop from an empty stack.")
        return self._list.remove_first()

    def peek(self) -> T:
        if self.empty:
            raise IndexError("Peek from an empty stack.")
        return self._list.first()

    @property
    def empty(self) -> bool:
        return len(self._list) == 0

    def clear(self):
        self._list.clear()

    def __contains__(self, item: T) -> bool:
        return item in self._list

    def __eq__(self, other) -> bool:
        if not isinstance(other, ListStack):
            return False
        return self._list == other._list

    def __len__(self) -> int:
        return len(self._list)

    def __str__(self) -> str:
        return str(self._list)

    def __repr__(self) -> str:
        return f"ListStack({repr(self._list)})"
