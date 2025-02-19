from __future__ import annotations
from collections.abc import Sequence, Iterator
import numpy as np
from numpy.typing import NDArray
from datastructures.iarray import IArray, T


class Array(IArray[T]):  
    def __init__(self, starting_sequence: Sequence[T] = [], data_type: type = object) -> None:
        """Initialize a dynamic array using NumPy."""
        if not isinstance(starting_sequence, Sequence):
            raise ValueError("Starting sequence must be a valid sequence type.")

        self._data_type = data_type
        self._logical_size = len(starting_sequence)
        self._physical_size = max(2, self._logical_size * 2)  
        self._array: NDArray = np.empty(self._physical_size, dtype=self._data_type)

        for i, item in enumerate(starting_sequence):
            if not isinstance(item, self._data_type):
                raise TypeError(f"Expected type {self._data_type}, but got {type(item)}")  
            self._array[i] = item

    def __len__(self) -> int:
        """Return the logical size of the array."""
        return self._logical_size

    def __getitem__(self, index: int | slice) -> T | Array[T]:
        """Retrieve an item or slice from the array."""
        if isinstance(index, int):
            if index < 0:
                index += self._logical_size
            if index < 0 or index >= self._logical_size:
                raise IndexError("Array index out of bounds.")
            return self._array[index].item() if isinstance(self._array[index], np.generic) else self._array[index]

        if isinstance(index, slice):
            return Array(
                starting_sequence=[x.item() if isinstance(x, np.generic) else x for x in self._array[index][:self._logical_size]],
                data_type=self._data_type
            )

        raise TypeError("Index must be an integer or a slice.")

    def __setitem__(self, index: int, item: T) -> None:
        """Modify an item at a specific index."""
        if not isinstance(item, self._data_type):
            raise TypeError(f"Expected type {self._data_type}, but got {type(item)}")  
        if index < 0:
            index += self._logical_size
        if index < 0 or index >= self._logical_size:
            raise IndexError("Array index out of bounds.")
        self._array[index] = item

    def append(self, data: T) -> None:
        """Append an item to the end of the array, resizing if necessary."""
        if self._logical_size == self._physical_size:
            self._resize(self._physical_size * 2)

        self._array[self._logical_size] = data
        self._logical_size += 1

    def append_front(self, data: T) -> None:
        """Append an item to the front of the array."""
        if self._logical_size == self._physical_size:
            self._resize(self._physical_size * 2)

        self._array[1 : self._logical_size + 1] = self._array[0 : self._logical_size]
        self._array[0] = data
        self._logical_size += 1

    def pop(self) -> None:
        """Remove the last element and shrink array if necessary."""
        if self._logical_size == 0:
            raise IndexError("Pop from empty array.")
        self._logical_size -= 1
        if self._logical_size <= self._physical_size // 4:
            self._resize(self._physical_size // 2)

    def pop_front(self) -> None:
        """Remove the first element and shift elements left."""
        if self._logical_size == 0:
            raise IndexError("Pop from empty array.")
        self._array[: self._logical_size - 1] = self._array[1 : self._logical_size]
        self._logical_size -= 1
        if self._logical_size <= self._physical_size // 4:
            self._resize(self._physical_size // 2)

    def __delitem__(self, index: int) -> None:
        """Delete an item at an index and shift elements left."""
        if index < 0:
            index += self._logical_size
        if index < 0 or index >= self._logical_size:
            raise IndexError("Array index out of bounds.")

        self._array[index:self._logical_size - 1] = self._array[index + 1:self._logical_size]
        self._logical_size -= 1

        if self._logical_size <= self._physical_size // 4:
            self._resize(self._physical_size // 2)

    def __eq__(self, other: object) -> bool:
        """Check equality of two arrays."""
        if not isinstance(other, Array):
            return False
        return np.array_equal(self._array[:self._logical_size], other._array[:other._logical_size])

    def __iter__(self) -> Iterator[T]:
        """Return an iterator over the array."""
        return iter(self._array[:self._logical_size])

    def __reversed__(self) -> Iterator[T]:
        """Return a reversed iterator."""
        return iter(self._array[:self._logical_size][::-1])

    def __contains__(self, item: T) -> bool:
        """Check if an item exists in the array."""
        return item in self._array[:self._logical_size]

    def clear(self) -> None:
        """Clear the array."""
        self._logical_size = 0

    def __str__(self) -> str:
        """Return a string representation of the array."""
        return str(list(self._array[:self._logical_size]))

    def __repr__(self) -> str:
        """Return a detailed string representation of the array."""
        return f"Array(logical size: {self._logical_size}, physical size: {self._physical_size}, data type: {self._data_type})"

    def _resize(self, new_size: int) -> None:
        """Resize the array to a new size."""
        new_array = np.empty(new_size, dtype=self._data_type)
        new_array[: self._logical_size] = self._array[: self._logical_size]
        self._array = new_array
        self._physical_size = new_size
