from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Sequence, Iterator
from datastructures.ilinkedlist import ILinkedList, T


class LinkedList(ILinkedList[T]):

    @dataclass
    class Node:
        data: T
        next: Optional[LinkedList.Node] = None
        previous: Optional[LinkedList.Node] = None

    def __init__(self, data_type: type = object) -> None:
        self.head: Optional[LinkedList.Node] = None
        self.tail: Optional[LinkedList.Node] = None
        self.count = 0
        self.data_type = data_type
        self._iter_node: Optional[LinkedList.Node] = None

    @staticmethod
    def from_sequence(sequence: Sequence[T], data_type: type = object) -> LinkedList[T]:
        ll = LinkedList(data_type)
        for item in sequence:
            if not isinstance(item, data_type):
                raise TypeError("All elements must be of the specified data_type")
            ll.append(item)
        return ll

    def _validate_type(self, item: T) -> None:
        if not isinstance(item, self.data_type):
            raise TypeError("Item must match data_type")

    def append(self, item: T) -> None:
        self._validate_type(item)
        new_node = self.Node(item)
        if self.tail is None:
            self.head = self.tail = new_node
        else:
            self.tail.next = new_node
            new_node.previous = self.tail
            self.tail = new_node
        self.count += 1

    def prepend(self, item: T) -> None:
        self._validate_type(item)
        new_node = self.Node(item)
        if self.head is None:
            self.head = self.tail = new_node
        else:
            new_node.next = self.head
            self.head.previous = new_node
            self.head = new_node
        self.count += 1

    def insert_before(self, target: T, item: T) -> None:
        self._validate_type(item)
        self._validate_type(target)
        current = self.head
        while current:
            if current.data == target:
                new_node = self.Node(item, next=current, previous=current.previous)
                if current.previous:
                    current.previous.next = new_node
                else:
                    self.head = new_node
                current.previous = new_node
                self.count += 1
                return
            current = current.next
        raise ValueError("Target not found")

    def insert_after(self, target: T, item: T) -> None:
        self._validate_type(item)
        self._validate_type(target)
        current = self.head
        while current:
            if current.data == target:
                new_node = self.Node(item, next=current.next, previous=current)
                if current.next:
                    current.next.previous = new_node
                else:
                    self.tail = new_node
                current.next = new_node
                self.count += 1
                return
            current = current.next
        raise ValueError("Target not found")

    def remove(self, item: T) -> None:
        self._validate_type(item)
        current = self.head
        while current:
            if current.data == item:
                if current.previous:
                    current.previous.next = current.next
                else:
                    self.head = current.next
                if current.next:
                    current.next.previous = current.previous
                else:
                    self.tail = current.previous
                self.count -= 1
                return
            current = current.next
        raise ValueError("Item not found")

    def remove_all(self, item: T) -> None:
        self._validate_type(item)
        current = self.head
        while current:
            next_node = current.next
            if current.data == item:
                if current.previous:
                    current.previous.next = current.next
                else:
                    self.head = current.next
                if current.next:
                    current.next.previous = current.previous
                else:
                    self.tail = current.previous
                self.count -= 1
            current = next_node

    def pop(self) -> T:
        if self.tail is None:
            raise IndexError("List is empty")
        data = self.tail.data
        if self.tail.previous:
            self.tail = self.tail.previous
            self.tail.next = None
        else:
            self.head = self.tail = None
        self.count -= 1
        return data

    def pop_front(self) -> T:
        if self.head is None:
            raise IndexError("List is empty")
        data = self.head.data
        if self.head.next:
            self.head = self.head.next
            self.head.previous = None
        else:
            self.head = self.tail = None
        self.count -= 1
        return data

    @property
    def front(self) -> T:
        if self.head is None:
            raise IndexError("List is empty")
        return self.head.data

    @property
    def back(self) -> T:
        if self.tail is None:
            raise IndexError("List is empty")
        return self.tail.data

    @property
    def empty(self) -> bool:
        return self.count == 0

    def __len__(self) -> int:
        return self.count

    def clear(self) -> None:
        self.head = self.tail = None
        self.count = 0

    def __contains__(self, item: T) -> bool:
        current = self.head
        while current:
            if current.data == item:
                return True
            current = current.next
        return False

    def __iter__(self) -> Iterator[T]:
        self._iter_node = self.head
        return self

    def __next__(self) -> T:
        if self._iter_node is None:
            raise StopIteration
        data = self._iter_node.data
        self._iter_node = self._iter_node.next
        return data

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, LinkedList):
            return False
        return list(self) == list(other)

    def __reversed__(self) -> LinkedList[T]:
        reversed_list = LinkedList(self.data_type)
        current = self.tail
        while current:
            reversed_list.append(current.data)
            current = current.previous
        return reversed_list

    def __str__(self) -> str:
        return '(' + ' <-> '.join(str(item) for item in self) + ')'

    def __repr__(self) -> str:
        return f"LinkedList({' <-> '.join(str(item) for item in self)}) Count: {self.count}"

    # === Aliases for compatibility with ListStack and Deque ===
    def remove_first(self) -> T:
        return self.pop_front()

    def remove_last(self) -> T:
        return self.pop()

    def first(self) -> T:
        return self.front

    def last(self) -> T:
        return self.back





