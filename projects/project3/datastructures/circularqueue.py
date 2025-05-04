from typing import Generic, List, TypeVar
from datastructures.iqueue import IQueue

T = TypeVar('T')

class CircularQueue(IQueue[T], Generic[T]):
    def __init__(self, maxsize: int = 0, data_type=object) -> None:
        if maxsize <= 0:
            raise ValueError("maxsize must be greater than 0")
        self._maxsize = maxsize
        self._data_type = data_type
        self.circularqueue: List[T] = [None] * maxsize
        self._front = 0
        self._rear = 0
        self._size = 0

    def enqueue(self, item: T) -> None:
        if self.full:
            raise IndexError("Queue is full")
        self.circularqueue[self._rear] = item
        self._rear = (self._rear + 1) % self._maxsize
        self._size += 1

    def dequeue(self) -> T:
        if self.empty:
            raise IndexError("Queue is empty")
        item = self.circularqueue[self._front]
        self.circularqueue[self._front] = None  # Optional
        self._front = (self._front + 1) % self._maxsize
        self._size -= 1
        return item

    def clear(self) -> None:
        self.circularqueue = [None] * self._maxsize
        self._front = 0
        self._rear = 0
        self._size = 0

    @property
    def front(self) -> T:
        if self.empty:
            raise IndexError("Queue is empty")
        return self.circularqueue[self._front]

    @property
    def full(self) -> bool:
        return self._size == self._maxsize

    @property
    def empty(self) -> bool:
        return self._size == 0

    @property
    def maxsize(self) -> int:
        return self._maxsize

    def __len__(self) -> int:
        return self._size

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, CircularQueue):
            return False
        if self._data_type != other._data_type:
            return False
        if len(self) != len(other):
            return False

        for i in range(len(self)):
            self_index = (self._front + i) % self._maxsize
            other_index = (other._front + i) % other._maxsize
            if self.circularqueue[self_index] != other.circularqueue[other_index]:
                return False

        return True

    def __str__(self) -> str:
        elements = []
        for i in range(self._size):
            index = (self._front + i) % self._maxsize
            elements.append(self.circularqueue[index])
        return str(elements)

    def __repr__(self) -> str:
        return f'ArrayQueue({self.__str__()})'
