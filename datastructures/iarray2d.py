from typing import Any, TypeVar, Generic, Sequence
from collections.abc import Iterator
from abc import ABC, abstractmethod

T = TypeVar("T")  

class IArray2D(Generic[T], ABC):
    """Interface for a 2D Array data structure."""

    class IRow(Generic[T], ABC):
        """Interface for a single row within a 2D Array."""

        @abstractmethod
        def __getitem__(self, column_index: int) -> T:
            """Returns the value at the given column index."""
            pass

        @abstractmethod
        def __setitem__(self, column_index: int, value: T) -> None:
            """Sets the value at the given column index."""
            pass

        @abstractmethod
        def __iter__(self) -> Iterator[T]:
            """Returns an iterator over the row's values."""
            pass

        @abstractmethod
        def __reversed__(self) -> Iterator[T]:
            """Returns a reversed iterator over the row's values."""
            pass

        @abstractmethod
        def __len__(self) -> int:
            """Returns the number of columns in the row."""
            pass

        @abstractmethod
        def __str__(self) -> str:
            """Returns a string representation of the row."""
            pass

        @abstractmethod
        def __repr__(self) -> str:
            """Returns a detailed string representation of the row."""
            pass

    @abstractmethod
    def __init__(self, starting_sequence: Sequence[Sequence[T]], data_type=object) -> None:
        """Initializes the 2D array with the given sequence."""
        pass

    @staticmethod
    @abstractmethod
    def empty(rows: int = 0, cols: int = 0, data_type: type = object) -> "IArray2D":
        """Creates an empty 2D array of given dimensions."""
        pass

    @abstractmethod
    def __getitem__(self, row_index: int) -> IRow[T]:
        """Returns the row at the given index."""
        pass

    @abstractmethod
    def __iter__(self) -> Iterator[Sequence[T]]:
        """Returns an iterator over the rows."""
        pass

    @abstractmethod
    def __reversed__(self) -> Iterator[Sequence[T]]:
        """Returns a reversed iterator over the rows."""
        pass

    @abstractmethod
    def __len__(self) -> int:
        """Returns the number of rows in the array."""
        pass

    @abstractmethod
    def __str__(self) -> str:
        """Returns a string representation of the 2D array."""
        pass

    @abstractmethod
    def __repr__(self) -> str:
        """Returns a detailed string representation of the 2D array."""
        pass
