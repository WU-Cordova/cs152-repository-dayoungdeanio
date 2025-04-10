from typing import Iterable, Optional, Dict
from datastructures.ibag import IBag, T  


class Bag(IBag[T]):
    def __init__(self, *items: Optional[Iterable[T]]) -> None:
        self._items: Dict[T, int] = {}
        if items:
            for iterable in items:
                if iterable:
                    for item in iterable:
                        self.add(item)

    def add(self, item: T) -> None:
        if item is None:
            raise TypeError("Item cannot be None")
        self._items[item] = self._items.get(item, 0) + 1

    def remove(self, item: T) -> None:
        if item not in self._items:
            raise ValueError("Item not found in Bag")
        self._items[item] -= 1
        if self._items[item] == 0:
            del self._items[item]

    def count(self, item: T) -> int:
        return self._items.get(item, 0)

    def __len__(self) -> int:
        return sum(self._items.values())

    def distinct_items(self) -> Iterable[T]:
        return self._items.keys()

    def __contains__(self, item: T) -> bool:
        return item in self._items

    def clear(self) -> None:
        self._items.clear()
