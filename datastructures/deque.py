from datastructures.iqueue import IQueue
from datastructures.linkedlist import LinkedList
from typing import TypeVar, Generic

T = TypeVar("T")

class Deque(IQueue[T]):
    """
    A double-ended queue (deque) implementation.
    """

    def __init__(self, data_type: type = object) -> None:
        self._data_type = data_type
        self._list = LinkedList[T]()

    def enqueue(self, item: T) -> None:
        if not isinstance(item, self._data_type):
            raise TypeError(f"Expected {self._data_type}, got {type(item)}")
        self._list.append(item)

    def dequeue(self) -> T:
        if self.empty():
            raise IndexError("Deque is empty")
        return self._list.remove_first()

    def enqueue_front(self, item: T) -> None:
        if not isinstance(item, self._data_type):
            raise TypeError(f"Expected {self._data_type}, got {type(item)}")
        self._list.prepend(item)

    def dequeue_back(self) -> T:
        if self.empty():
            raise IndexError("Deque is empty")
        return self._list.remove_last()

    def front(self) -> T:
        if self.empty():
            raise IndexError("Deque is empty")
        return self._list.first()

    def back(self) -> T:
        if self.empty():
            raise IndexError("Deque is empty")
        return self._list.last()

    def empty(self) -> bool:
        return len(self._list) == 0

    def __len__(self) -> int:
        return len(self._list)

    def __contains__(self, item: T) -> bool:
        return item in self._list

    def __eq__(self, other) -> bool:
        if not isinstance(other, Deque):
            return False
        return self._list == other._list

    def clear(self):
        self._list.clear()

    def __str__(self) -> str:
        return str(self._list)

    def __repr__(self) -> str:
        return f"Deque({repr(self._list)})"
