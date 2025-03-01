from __future__ import annotations
from typing import Iterator, Sequence, TypeVar, Generic
from datastructures.iarray2d import IArray2D, T

T = TypeVar("T")

class Array2D(IArray2D[T]):
    class Row(IArray2D.IRow[T]):
        def __init__(self, row_index: int, array: Array2D[T], num_columns: int) -> None:
            self.row_index = row_index
            self.array = array
            self.num_columns = num_columns

        def __getitem__(self, column_index: int) -> T:
            if column_index < 0 or column_index >= self.num_columns:
                raise IndexError("Column index out of bounds")
            return self.array._data[self.row_index][column_index]
        
        def __setitem__(self, column_index: int, value: T) -> None:
            if column_index < 0 or column_index >= self.num_columns:
                raise IndexError("Column index out of bounds")
            self.array._data[self.row_index][column_index] = value
        
        def __iter__(self) -> Iterator[T]:
            return iter(self.array._data[self.row_index])
        
        def __reversed__(self) -> Iterator[T]:
            return reversed(self.array._data[self.row_index])

        def __len__(self) -> int:
            return self.num_columns
        
        def __str__(self) -> str:
            return f"[{', '.join(map(str, self.array._data[self.row_index]))}]"
        
        def __repr__(self) -> str:
            return f"Row {self.row_index}: {self}"

    def __init__(self, starting_sequence: Sequence[Sequence[T]] = [[]], data_type=object) -> None:
        """Initializes the 2D array, validating input data."""
        if not isinstance(starting_sequence, Sequence) or any(not isinstance(row, Sequence) for row in starting_sequence):
            raise ValueError("Starting sequence must be a sequence of sequences.")

        if any(any(not isinstance(item, data_type) for item in row) for row in starting_sequence):
            raise ValueError("All elements in starting_sequence must be of the same data type.")

        row_lengths = {len(row) for row in starting_sequence}
        if len(row_lengths) > 1:
            raise ValueError("All rows must have the same length.")

        self._data = [list(row) for row in starting_sequence]
        self.__num_rows = len(self._data)
        self.__num_columns = row_lengths.pop() if self.__num_rows > 0 else 0
        self.data_type = data_type

    @staticmethod
    def empty(rows: int = 0, cols: int = 0, data_type: type = object) -> Array2D:
        """Creates an empty Array2D of given dimensions and data type."""
        return Array2D([[data_type() for _ in range(cols)] for _ in range(rows)], data_type=data_type)

    def __getitem__(self, row_index: int) -> Row[T]:
        """Returns a row at the specified index."""
        if row_index < 0 or row_index >= self.__num_rows:
            raise IndexError("Row index out of bounds")
        return Array2D.Row(row_index, self, self.__num_columns)
    
    def __iter__(self) -> Iterator[Sequence[T]]:
        """Returns an iterator over the rows."""
        return iter(self._data)
    
    def __reversed__(self) -> Iterator[Sequence[T]]:
        """Returns a reversed iterator over the rows."""
        return reversed(self._data)
    
    def __len__(self) -> int:
        """Returns the number of rows in the 2D array."""
        return self.__num_rows
                                  
    def __str__(self) -> str:
        """Returns a string representation of the 2D array."""
        return f"[{', '.join(str(row) for row in self._data)}]"
    
    def __repr__(self) -> str:
        """Returns a detailed string representation of the 2D array."""
        return f"Array2D {self.__num_rows} Rows x {self.__num_columns} Columns, items: {str(self)}"
